#!/usr/bin/env python3
"""
Weather MCP Server
==================

A Model Context Protocol (MCP) server that provides real-time weather information 
using the OpenWeatherMap API.

Features:
- Fetches current weather data for a given city.
- gracefully handles API errors.
- Supports a Demo/Mock mode for testing without an API key.
"""

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("weather-mcp")

# Load environment variables
load_dotenv()

# Constants
DEFAULT_API_KEY = "c47b5207069c5f86bf41716e4b8034e0"  # Provided/Demo key
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@dataclass
class WeatherConfig:
    """Configuration settings for the Weather Server."""
    api_key: str
    demo_mode: bool = False

    @classmethod
    def from_env(cls) -> "WeatherConfig":
        """Load configuration from environment variables."""
        api_key = os.getenv("OPENWEATHER_API_KEY", DEFAULT_API_KEY)
        # Default to demo mode if the key looks like the default invalid one or is missing
        # For this specific user request, we check if it is explicitly set or fallback.
        # User prompt implies cleaning up, so let's allow explicit override.
        demo_mode_env = os.getenv("MCP_WEATHER_DEMO_MODE", "").lower() == "true"
        return cls(api_key=api_key, demo_mode=demo_mode_env)


class WeatherService:
    """Service to handle Weather API interactions."""

    def __init__(self, config: WeatherConfig):
        self.config = config
        self.session = requests.Session()

    def _get_mock_coordinates(self, city: str) -> Tuple[float, float]:
        """Return mock coordinates for testing."""
        city_lower = city.lower().strip()
        mock_data = {
            "london": (51.5074, -0.1278),
            "new york": (40.7128, -74.0060),
            "paris": (48.8566, 2.3522),
            "tokyo": (35.6762, 139.6503),
            "sydney": (-33.8688, 151.2093),
            "chennai": (13.0827, 80.2707),
        }
        
        # Exact match
        if city_lower in mock_data:
            return mock_data[city_lower]
            
        # Partial match
        for key, coords in mock_data.items():
            if key in city_lower or city_lower in key:
                return coords
                
        # Default fallback
        logger.info(f"Mock city not found: {city}. Defaulting to London.")
        return 51.5074, -0.1278

    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """Return mock weather data."""
        return {
            "main": {
                "temp": 22.5,
                "feels_like": 24.1,
                "humidity": 65,
                "pressure": 1012
            },
            "wind": {"speed": 3.5, "deg": 180},
            "weather": [{"main": "Clear", "description": "clear sky", "icon": "01d"}],
            "visibility": 10000,
            "name": city.title()
        }

    def get_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
        """Resolve city name to latitude and longitude."""
        if self.config.demo_mode:
            return self._get_mock_coordinates(city)

        try:
            params = {
                "q": city,
                "limit": 1,
                "appid": self.config.api_key
            }
            response = self.session.get(GEOCODING_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                logger.warning(f"No coordinates found for city: {city}")
                return None
                
            return data[0]["lat"], data[0]["lon"]
            
        except requests.RequestException as e:
            logger.error(f"Geocoding API error: {e}")
            return None

    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Fetch current weather for coordinates."""
        if self.config.demo_mode:
            return self._get_mock_weather("Demo City")

        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.config.api_key,
                "units": "metric"
            }
            response = self.session.get(WEATHER_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Weather API error: {e}")
            return None

    @staticmethod
    def format_response(city: str, data: Dict[str, Any]) -> str:
        """Format raw weather data into a human-readable string."""
        try:
            main = data.get("main", {})
            weather = data.get("weather", [{}])[0]
            wind = data.get("wind", {})
            
            temp = main.get("temp", "N/A")
            feels_like = main.get("feels_like", "N/A")
            condition = weather.get("main", "Unknown")
            description = weather.get("description", "Unknown")
            humidity = main.get("humidity", "N/A")
            wind_speed = wind.get("speed", "N/A")
            
            # Visibility conversion (meters to km)
            visibility_m = data.get("visibility")
            visibility_str = f"{visibility_m / 1000:.1f} km" if visibility_m else "N/A"

            return (
                f"### Weather for {city.title()}\n\n"
                f"- **Temperature:** {temp}°C (Feels like {feels_like}°C)\n"
                f"- **Condition:** {condition} ({description})\n"
                f"- **Humidity:** {humidity}%\n"
                f"- **Wind:** {wind_speed} m/s\n"
                f"- **Visibility:** {visibility_str}"
            )
        except Exception as e:
            logger.error(f"Formatting error: {e}")
            return f"Error processing weather data for {city}."


# Initialize Configuration and Service
config = WeatherConfig.from_env()
# Auto-enable demo mode if the API key is the known invalid default and user hasn't specified otherwise
if config.api_key == DEFAULT_API_KEY:
    logger.info("Using Default/Invalid API Key -> Switching to DEMO MODE")
    config.demo_mode = True

weather_service = WeatherService(config)

# Initialize MCP Server
app = FastMCP(
    "weather-mcp", 
    instructions="Provides weather information. Use 'get_weather' to fetch details for a specific city."
)


@app.tool()
def get_weather(city: str) -> str:
    """
    Fetch the current weather for a specific city.

    Args:
        city: The name of the city (e.g., "Paris, France", "Tokyo").

    Returns:
        A formatted string containing the weather details.
    """
    if not city or not city.strip():
        return "Error: City name cannot be empty."

    logger.info(f"Received request for city: {city}")
    
    # 1. Get Coordinates
    coords = weather_service.get_coordinates(city)
    if not coords:
        return f"Could not find coordinates for '{city}'. Please check the spelling."

    # 2. Get Weather Data
    data = weather_service.get_current_weather(coords[0], coords[1])
    if not data:
        return f"Failed to retrieve weather data for '{city}'."

    # 3. Format Response
    return weather_service.format_response(city, data)


if __name__ == "__main__":
    logger.info("Starting Weather MCP Server...")
    app.run(transport="stdio")
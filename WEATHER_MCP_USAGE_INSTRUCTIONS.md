# 🌦️ Weather MCP Server - Detailed Usage Guide

This document provides comprehensive instructions for using the Weather MCP Server in various environments. This server is designed as a robust Proof of Concept (POC) for the Model Context Protocol.

## 📋 Overview

The Weather MCP Server allows AI models to fetch real-time weather information. It acts as a bridge between your AI assistant (like Claude or Cursor) and the OpenWeatherMap API.

### Key Features
- **Auto-Switching Demo Mode**: If no valid API key is present, the server automatically serves mock data for testing.
- **Resilient Geocoding**: Converts city names to coordinates handles errors gracefully.
- **Rich Output**: Returns formatted markdown summaries of weather conditions.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10 or newer installed.
- `pip` package manager.

### 2. Check Dependencies
Ensure valid dependencies are installed:
```bash
pip install -r requirements.txt
```

### 3. API Key Configuration (Optional)
By default, the server runs in **Demo Mode** using a placeholder key. To access real weather data:

1. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api).
2. Set the environment variable `OPENWEATHER_API_KEY`.
   - **Option A**: Create a `.env` file in the project root:
     ```env
     OPENWEATHER_API_KEY=your_actual_api_key_here
     ```
   - **Option B**: Pass it inline (Linux/Mac):
     ```bash
     OPENWEATHER_API_KEY=your_key python weather_mcp_server.py
     ```

---

## 🔧 Integration Guides

### 1. Claude Desktop (Anthropic)
To use this server with the Claude Desktop app, edit your configuration file.

- **Location**:
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

- **Configuration**:
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "D:\\windsuf-prac\\MCPs\\weather-mcp\\weather_mcp_server.py"
      ]
    }
  }
}
```

### 2. Cursor IDE
Cursor has native support for MCP.

1. Open **Cursor Settings** (Ctrl+Shift+J or Cmd+Shift+J) > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Fill in the fields:
   - **Name**: `weather-local`
   - **Type**: `stdio`
   - **Command**: `python D:\windsuf-prac\MCPs\weather-mcp\weather_mcp_server.py`
4. Click **Save** and ensure the status indicator turns green.

### 3. VS Code (Generic MCP Extension)
If you are using a generic MCP extension in VS Code, add this to your `.vscode/settings.json` or user settings:

```json
{
  "mcp.servers": {
    "weather": {
      "command": "python",
      "args": ["D:\\windsuf-prac\\MCPs\\weather-mcp\\weather_mcp_server.py"]
    }
  }
}
```

---

## 📚 API Reference

### Tool: `get_weather`
The server exposes one primary tool to the LLM.

**Signature**:
```python
def get_weather(city: str) -> str:
```

**Parameters**:
- `city` (string): The name of the city to lookup (e.g., "Paris", "New York, US").

**Returns**:
A formatted Markdown string containing:
- Temperature & Feels Like (°C)
- Weather Condition (e.g., "Clear", "Rain")
- Humidity (%)
- Wind Speed (m/s)
- Visibility (km)

**Example Output**:
```markdown
### Weather for Tokyo

- **Temperature:** 22.5°C (Feels like 24.1°C)
- **Condition:** Clear (clear sky)
- **Humidity:** 65%
- **Wind:** 3.5 m/s
- **Visibility:** 10.0 km
```

---

## 🔍 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **Receiving Mock Data** | API Key is missing or invalid. | Check your `.env` file or export `OPENWEATHER_API_KEY`. |
| **Server Error on Start** | Missing dependencies. | Run `pip install -r requirements.txt`. |
| **"City not found"** | Typos in city name. | Check spelling. In Demo Mode, supports major cities like London, Paris, Tokyo. |
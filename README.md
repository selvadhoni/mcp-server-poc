# 🌦️ Weather MCP Server (POC)

A robust, production-ready Proof of Concept (POC) for a **Model Context Protocol (MCP)** server. This server connects to the OpenWeatherMap API to provide real-time weather information to AI agents and MCP clients.

## 🚀 Features

- **Real-Time Weather data**: Fetches current temperature, humidity, wind speed, and conditions.
- **Auto-Detect Demo Mode**: Automatically switches to mock data if no valid API Key is found, ensuring the server is testable immediately out of the box.
- **Robust Error Handling**: Gracefully handles API failures and invalid inputs.
- **Type-Safe & Clean**: Built with modern Python practices, type hinting, and modular architecture.

---

## 🛠️ Prerequisites

- **Python 3.10** or higher.
- (Optional) An [OpenWeatherMap API Key](https://openweathermap.org/api) for real data.

## 📦 Installation

1. **Clone/Navigate to the directory**:
   ```bash
   cd D:\windsuf-prac\MCPs\weather-mcp
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

The server works immediately without configuration (in Demo Mode). To use real data:

1. Create a `.env` file in the root directory (optional):
   ```env
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```
2. Or set the environment variable explicitly when running.

---

## 🏃‍♂️ Usage

You can run the server directly using Python. It relies on `stdio` (standard input/output) to communicate with MCP clients.

```bash
python weather_mcp_server.py
```

### 🔌 Connecting to MCP Clients

#### 1. Claude Desktop App
Add the following configuration to your `claude_desktop_config.json`:

**Windows** (`%APPDATA%\Claude\claude_desktop_config.json`):
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
*Note: Ensure you use the full absolute path to the python script.*

#### 2. Cursor IDE
1. Go to **Cursor Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Enter the details:
   - **Name**: `Weather POC`
   - **Type**: `stdio`
   - **Command**: `python D:\windsuf-prac\MCPs\weather-mcp\weather_mcp_server.py`

#### 3. Testing
Once connected, you can ask your AI assistant:
> "What is the weather in Tokyo?"
> "Get me the current weather for London."

---

## 🛠️ Project Structure

```
weather-mcp/
├── weather_mcp_server.py       # Main server logic (Senior-grade refactor)
├── requirements.txt            # Project dependencies
├── README.md                   # This documentation
└── WEATHER_MCP_USAGE_INSTRUCTIONS.md  # (Legacy) Detailed usage archive
```

## 🧩 Tools Available

### `get_weather(city: str)`
Fetches standard weather metrics for a specified city.
- **Calculates**: Temperature, Feels Like, Humidity, Wind Speed, Visibility.
- **Returns**: A pre-formatted Markdown summary.

---

## 🔍 Troubleshooting

- **Server crashes immediately?**
  Ensure dependencies are installed: `pip install -r requirements.txt`
  
- **Getting "Mock City" results?**
  The server is in **Demo Mode**. This happens if the `OPENWEATHER_API_KEY` is missing or set to the default placeholder. Add a valid key to `.env` to fix.

- **"Command not found"?**
  Ensure `python` is in your system PATH or use the full path to your python executable (e.g., `C:\Python310\python.exe`).

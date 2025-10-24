# 🗺️ Geospatial & Cadastral MCP Server

**Unified access to Dutch geospatial, cadastral, and topographical data**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)

Access comprehensive Dutch geospatial data from PDOK (Publieke Dienstverlening Op de Kaart) and Kadaster through Claude Desktop. Query addresses, building heights, cadastral parcels, noise data, and administrative boundaries.

---

## 🌍 Available Data Sources (8 APIs)

| API | Description | Example Use |
|-----|-------------|-------------|
| **PDOK Location Server** | Search addresses, parcels, and locations | "Find all addresses on Damrak" |
| **BAG Registry** | Detailed building and address data | "Get building details for address X" |
| **Kadastrale Kaart** | Cadastral parcel boundaries (GeoJSON) | "Show parcel boundaries" |
| **3D Basisvoorziening** | 3D building heights (AHN4 data) | "What's the height of this building?" |
| **3D Geluid** | Environmental noise modeling data | "Get noise levels near highway" |
| **BGT/BRT** | Base Registration Topography | "Show topographical features" |
| **Bestuurlijke Gebieden** | Administrative boundaries | "Find municipality boundaries" |
| **Coordinate Converter** | RD ↔ WGS84 conversion | "Convert these coordinates" |

> 📍 All coordinates returned in both **RD (EPSG:28992)** and **WGS84 (EPSG:4326)** formats

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- No API key required (uses public PDOK services)

### 1️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/TCLUBNL/geospatial-cadastral-mcp-server.git
cd geospatial-cadastral-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Test the Server

```bash
python3 -c "from server.tools.search_location import search_location; r = search_location('Damrak 1, Amsterdam'); print(f'✅ Found: {r["results"][0]["display_name"]}')"
```

Expected output: `✅ Found: Damrak 1, 1012JS Amsterdam`

---

## 🔌 Claude Desktop Integration

### Step 1: Find Your Config File

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### Step 2: Add Server Configuration

Replace `/absolute/path/to/` with your actual paths:

```json
{
  "mcpServers": {
    "geospatial-cadastral": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/geospatial-cadastral-mcp-server/mcp_server_simple.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/geospatial-cadastral-mcp-server"
      }
    }
  }
}
```

> 💡 **Tip:** Use `pwd` in your terminal to get the absolute path.

### Step 3: Restart Claude Desktop

Quit Claude Desktop completely and reopen it. You should see the 🔌 icon indicating MCP servers are connected.

### Step 4: Test in Claude

Try these example queries:

- *"Find the address Damrak 1 in Amsterdam"*
- *"What's the height of the building at this address?"*
- *"Show me cadastral parcel boundaries for this location"*
- *"Convert RD coordinates 121000, 487000 to WGS84"*
- *"Get noise data near Schiphol airport"*

---

## 📡 Available Tools

| Tool | Description | Example Use |
|------|-------------|-------------|
| `search_location` | Find addresses, parcels, locations | Search for any Dutch address |
| `get_bag_address` | Detailed building information | Get construction year, surface area |
| `get_cadastral_parcel` | Parcel boundaries with GeoJSON | Visualize property boundaries |
| `get_3d_building_data` | Building heights from AHN4 | Get elevation and height data |
| `get_noise_data` | Environmental noise levels | Check noise pollution |
| `get_topography` | BGT/BRT topographical data | Get terrain features |
| `get_administrative_boundaries` | Municipality borders | Find administrative regions |
| `validate_coordinates` | RD ↔ WGS84 conversion | Convert between coordinate systems |

---

## 🧠 Architecture

```
┌─────────────────────────────────────────┐
│   Claude Desktop (MCP Host)             │
│   ┌─────────────────────────────────┐   │
│   │ Geospatial & Cadastral Client   │   │
│   └──────────────┬──────────────────┘   │
└──────────────────┼──────────────────────┘
                   │ MCP Protocol (stdio)
┌──────────────────┼──────────────────────┐
│                  ▼                       │
│   Geospatial & Cadastral MCP Server     │
│   ┌─────────────────────────────────┐   │
│   │  8 Tools for Dutch Geo Data     │   │
│   └──────────────┬──────────────────┘   │
└──────────────────┼──────────────────────┘
                   │ HTTPS
        ┌──────────┼──────────┐
        ▼          ▼           ▼
    ┌─────┐   ┌─────────┐  ┌──────────┐
    │PDOK │   │Kadaster │  │  AHN4    │
    └─────┘   └─────────┘  └──────────┘
```

---

## ⚠️ Known Limitations

- **Rate Limits:** PDOK services have standard rate limits
- **Coverage:** Data is specific to the Netherlands only
- **3D Data:** Building height data availability varies by region
- **Coordinate Systems:** Primarily uses Dutch RD (EPSG:28992) with WGS84 conversion

---

## 🔗 Related MCP Servers

- **[Amsterdam Municipal MCP](https://github.com/TCLUBNL/amsterdam-municipal-mcp-server)** - Amsterdam-specific data (addresses, neighborhoods, waste containers)
- **[CBS Statistics MCP](https://github.com/TCLUBNL/cbs-statistics-mcp-server)** - Dutch national statistics

---

## 📝 License

MIT License • Data sourced from Dutch government open data (PDOK, Kadaster)

**Data Sources:**
- [PDOK](https://www.pdok.nl) - Dutch Public Services On the Map
- [Kadaster](https://www.kadaster.nl) - Dutch Land Registry

---

## 🤝 Contributing

Issues and pull requests are welcome! Feel free to contribute improvements or report bugs.

---

**Built with ❤️ by [TCLUB NL](https://github.com/TCLUBNL)**

⭐ **Star this repo** if you find it useful!
# 🗺️ Geospatial & Cadastral MCP Server

**Unified access to Dutch geospatial, cadastral, and topographical data APIs**

This project implements an **MCP (Model Context Protocol)** server providing structured access to geospatial data from **PDOK (Publieke Dienstverlening Op de Kaart)** and the **Dutch Kadaster** (Cadastre).

---

## 🧠 Architecture Overview

**Client:** Geospatial & Cadastral MCP Client
- Lives inside an MCP host (e.g., Claude Desktop)
- Uses the defined manifest to understand available tools
- Sends queries to the Geospatial MCP Server for spatial data retrieval

**Server:** Geospatial & Cadastral MCP Server (this project)
- Built using Python (stdio-based MCP protocol)
- Provides unified access to 8+ Dutch geospatial APIs
- Returns coordinates in both RD (EPSG:28992) and WGS84 (EPSG:4326)

---

## 🌍 APIs Included

| API | Description | Example Use |
|-----|-------------|-------------|
| **PDOK Location Server** | Search addresses, parcels, and locations | Find addresses |
| **BAG Registry** | Detailed building data | Building details |
| **Kadastrale Kaart** | Cadastral parcel boundaries | Parcel info |
| **3D Basisvoorziening** | 3D building heights | Height data |
| **3D Geluid** | Noise modeling data | Noise levels |
| **BGT/BRT** | Topography | Maps |
| **Bestuurlijke Gebieden** | Administrative boundaries | Municipality data |
| **Coordinate Converter** | Convert RD to WGS84 | Coordinate conversion |

---

## 🚀 Quick Start

1. Create virtual environment: python3 -m venv venv
2. Activate: source venv/bin/activate
3. Install: pip install -r requirements.txt
4. Test: python3 mcp_server_simple.py

---

## 🔌 Claude Desktop Integration

Edit ~/Library/Application Support/Claude/claude_desktop_config.json

Add server configuration with your username path.

---

## 📡 Available Tools

1. search_location - Find addresses and parcels
2. get_bag_address - Building details
3. get_cadastral_parcel - Parcel boundaries
4. get_3d_building_data - Building heights
5. get_noise_data - Noise levels
6. get_topography - Topographical features
7. get_administrative_boundaries - Municipality boundaries
8. validate_coordinates - Coordinate conversion

---

## 📝 License

Open source. Data from Dutch government sources.

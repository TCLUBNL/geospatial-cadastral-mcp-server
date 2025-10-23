#!/usr/bin/env python3
"""
MCP stdio server for Geospatial & Cadastral data
Implements MCP protocol over stdio (JSON-RPC)
"""

import json
import sys
import logging

# Set up logging to stderr (will appear in Claude logs)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Import tools at module level to catch import errors early
try:
    from server.tools.search_location import search_location
    from server.tools.get_bag_address import get_bag_address
    from server.tools.get_cadastral_parcel import get_cadastral_parcel
    from server.tools.get_3d_building_data import get_3d_building_data
    from server.tools.get_noise_data import get_noise_data
    from server.tools.get_topography import get_topography
    from server.tools.get_administrative_boundaries import get_administrative_boundaries
    from server.tools.validate_coordinates import validate_coordinates
    logger.info("All tool modules imported successfully")
except Exception as e:
    logger.error(f"Failed to import tool modules: {str(e)}", exc_info=True)
    sys.exit(1)

def handle_request(request):
    """Handle incoming JSON-RPC requests"""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")
    
    logger.debug(f"Received: method={method}, id={request_id}, params={params}")
    
    try:
        if method == "initialize":
            client_protocol = params.get("protocolVersion", "2024-11-05")
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": client_protocol,
                    "capabilities": {
                        "tools": {},
                        "prompts": {},
                        "resources": {}
                    },
                    "serverInfo": {
                        "name": "geospatial-cadastral",
                        "version": "1.0.0"
                    }
                }
            }
            logger.info(f"Sent initialize response with protocol {client_protocol}")
            return result
        
        elif method == "initialized":
            logger.info("Received initialized notification")
            return None
            
        elif method == "tools/list":
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "search_location",
                            "description": "Search for addresses, cadastral parcels, or locations using PDOK Location Server",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Search query (address, postal code, parcel ID, or place name)"
                                    },
                                    "filter_type": {
                                        "type": "string",
                                        "description": "Optional filter: 'adres', 'perceel', 'postcode', 'gemeente', 'woonplaats'"
                                    }
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "get_bag_address",
                            "description": "Fetch detailed building and address data from BAG (Basisregistratie Adressen en Gebouwen)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "bag_id": {
                                        "type": "string",
                                        "description": "BAG identifier (if known)"
                                    },
                                    "postal_code": {
                                        "type": "string",
                                        "description": "Postal code (e.g., '1012JS')"
                                    },
                                    "house_number": {
                                        "type": "integer",
                                        "description": "House number"
                                    }
                                }
                            }
                        },
                        {
                            "name": "get_cadastral_parcel",
                            "description": "Fetch cadastral parcel data including boundaries, ownership info, and parcel numbers",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "parcel_id": {
                                        "type": "string",
                                        "description": "Cadastral parcel identifier (e.g., 'ASD01-A-1234')"
                                    },
                                    "x": {
                                        "type": "number",
                                        "description": "RD X-coordinate (EPSG:28992)"
                                    },
                                    "y": {
                                        "type": "number",
                                        "description": "RD Y-coordinate (EPSG:28992)"
                                    }
                                }
                            }
                        },
                        {
                            "name": "get_3d_building_data",
                            "description": "Fetch 3D building height and elevation data from 3D Basisvoorziening",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "x": {
                                        "type": "number",
                                        "description": "RD X-coordinate (EPSG:28992)"
                                    },
                                    "y": {
                                        "type": "number",
                                        "description": "RD Y-coordinate (EPSG:28992)"
                                    },
                                    "radius": {
                                        "type": "integer",
                                        "description": "Search radius in meters (default 100)"
                                    }
                                },
                                "required": ["x", "y"]
                            }
                        },
                        {
                            "name": "get_noise_data",
                            "description": "Fetch 3D noise modeling data for traffic and industrial noise",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "x": {
                                        "type": "number",
                                        "description": "RD X-coordinate (EPSG:28992)"
                                    },
                                    "y": {
                                        "type": "number",
                                        "description": "RD Y-coordinate (EPSG:28992)"
                                    },
                                    "noise_type": {
                                        "type": "string",
                                        "description": "Type: 'wegverkeerslawaai', 'railverkeerslawaai', 'industrielawaai'"
                                    }
                                },
                                "required": ["x", "y"]
                            }
                        },
                        {
                            "name": "get_topography",
                            "description": "Fetch topographical features from BGT (large-scale) or BRT/TOP10NL (base maps)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "x": {
                                        "type": "number",
                                        "description": "RD X-coordinate (EPSG:28992)"
                                    },
                                    "y": {
                                        "type": "number",
                                        "description": "RD Y-coordinate (EPSG:28992)"
                                    },
                                    "radius": {
                                        "type": "integer",
                                        "description": "Search radius in meters (default 500)"
                                    },
                                    "layer": {
                                        "type": "string",
                                        "description": "'bgt' for large-scale or 'top10nl' for base maps"
                                    }
                                },
                                "required": ["x", "y"]
                            }
                        },
                        {
                            "name": "get_administrative_boundaries",
                            "description": "Fetch administrative boundaries for municipalities, provinces, or other regions",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "admin_type": {
                                        "type": "string",
                                        "description": "Type: 'gemeente', 'provincie', 'waterschap'"
                                    },
                                    "name": {
                                        "type": "string",
                                        "description": "Optional name filter (e.g., 'Amsterdam')"
                                    }
                                },
                                "required": ["admin_type"]
                            }
                        },
                        {
                            "name": "validate_coordinates",
                            "description": "Convert and validate coordinates between RD (EPSG:28992) and WGS84 (EPSG:4326)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "x": {
                                        "type": "number",
                                        "description": "RD X-coordinate"
                                    },
                                    "y": {
                                        "type": "number",
                                        "description": "RD Y-coordinate"
                                    },
                                    "lat": {
                                        "type": "number",
                                        "description": "WGS84 latitude"
                                    },
                                    "lon": {
                                        "type": "number",
                                        "description": "WGS84 longitude"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
            logger.info("Sent tools/list response")
            return result
        
        elif method == "prompts/list":
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "prompts": []
                }
            }
            logger.info("Sent prompts/list response")
            return result
        
        elif method == "resources/list":
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "resources": []
                }
            }
            logger.info("Sent resources/list response")
            return result
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            logger.info(f"Calling tool: {tool_name}")
            
            if tool_name == "search_location":
                data = search_location(
                    query=arguments["query"],
                    filter_type=arguments.get("filter_type")
                )
            elif tool_name == "get_bag_address":
                data = get_bag_address(
                    bag_id=arguments.get("bag_id"),
                    postal_code=arguments.get("postal_code"),
                    house_number=arguments.get("house_number")
                )
            elif tool_name == "get_cadastral_parcel":
                data = get_cadastral_parcel(
                    parcel_id=arguments.get("parcel_id"),
                    x=arguments.get("x"),
                    y=arguments.get("y")
                )
            elif tool_name == "get_3d_building_data":
                data = get_3d_building_data(
                    x=arguments["x"],
                    y=arguments["y"],
                    radius=arguments.get("radius", 100)
                )
            elif tool_name == "get_noise_data":
                data = get_noise_data(
                    x=arguments["x"],
                    y=arguments["y"],
                    noise_type=arguments.get("noise_type", "wegverkeerslawaai")
                )
            elif tool_name == "get_topography":
                data = get_topography(
                    x=arguments["x"],
                    y=arguments["y"],
                    radius=arguments.get("radius", 500),
                    layer=arguments.get("layer", "bgt")
                )
            elif tool_name == "get_administrative_boundaries":
                data = get_administrative_boundaries(
                    admin_type=arguments["admin_type"],
                    name=arguments.get("name")
                )
            elif tool_name == "validate_coordinates":
                data = validate_coordinates(
                    x=arguments.get("x"),
                    y=arguments.get("y"),
                    lat=arguments.get("lat"),
                    lon=arguments.get("lon")
                )
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            result = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(data, indent=2, ensure_ascii=False)
                        }
                    ]
                }
            }
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        
        else:
            logger.warning(f"Unknown method: {method}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    except Exception as e:
        logger.error(f"Error in {method}: {str(e)}", exc_info=True)
        error_id = request_id if request_id is not None else 0
        return {
            "jsonrpc": "2.0",
            "id": error_id,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }

def main():
    """Main stdio loop"""
    logger.info("=== Geospatial & Cadastral MCP Server Starting ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {sys.path[0]}")
    
    try:
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    logger.info("EOF received, shutting down")
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                logger.debug(f"Received line: {line[:200]}...")
                
                request = json.loads(line)
                response = handle_request(request)
                
                if response is not None:
                    response_str = json.dumps(response)
                    print(response_str, flush=True)
                    logger.debug(f"Sent response: {response_str[:200]}...")
                    
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {str(e)}", exc_info=True)
                
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        logger.info("=== Server Shutdown ===")

if __name__ == "__main__":
    main()

from typing import Dict, Any, Tuple

def validate_coordinates(x: float = None, y: float = None, 
                        lat: float = None, lon: float = None) -> Dict[str, Any]:
    """
    Convert and validate coordinates between RD (EPSG:28992) and WGS84 (EPSG:4326).
    
    Args:
        x: RD X-coordinate (optional)
        y: RD Y-coordinate (optional)
        lat: WGS84 latitude (optional)
        lon: WGS84 longitude (optional)
    
    Returns:
        Dictionary containing converted coordinates and validation status
    """
    try:
        from pyproj import Transformer
        
        # Transformer from RD to WGS84
        rd_to_wgs84 = Transformer.from_crs("EPSG:28992", "EPSG:4326", always_xy=True)
        # Transformer from WGS84 to RD
        wgs84_to_rd = Transformer.from_crs("EPSG:4326", "EPSG:28992", always_xy=True)
        
        result = {
            "input": {},
            "output": {},
            "validation": {}
        }
        
        if x is not None and y is not None:
            # Convert RD to WGS84
            result["input"] = {"x_rd": x, "y_rd": y, "system": "RD (EPSG:28992)"}
            
            # Validate RD bounds (Netherlands approximately)
            valid_rd = (0 <= x <= 300000) and (300000 <= y <= 625000)
            result["validation"]["rd_in_bounds"] = valid_rd
            
            if valid_rd:
                lon_out, lat_out = rd_to_wgs84.transform(x, y)
                result["output"] = {
                    "latitude": lat_out,
                    "longitude": lon_out,
                    "system": "WGS84 (EPSG:4326)"
                }
            else:
                result["output"] = {"error": "RD coordinates out of Netherlands bounds"}
        
        elif lat is not None and lon is not None:
            # Convert WGS84 to RD
            result["input"] = {"latitude": lat, "longitude": lon, "system": "WGS84 (EPSG:4326)"}
            
            # Validate WGS84 bounds (Netherlands approximately)
            valid_wgs84 = (50.5 <= lat <= 53.7) and (3.2 <= lon <= 7.3)
            result["validation"]["wgs84_in_bounds"] = valid_wgs84
            
            if valid_wgs84:
                x_out, y_out = wgs84_to_rd.transform(lon, lat)
                result["output"] = {
                    "x_rd": x_out,
                    "y_rd": y_out,
                    "system": "RD (EPSG:28992)"
                }
            else:
                result["output"] = {"error": "WGS84 coordinates out of Netherlands bounds"}
        
        else:
            return {
                "error": "Either (x, y) for RD or (lat, lon) for WGS84 required",
                "example_rd": {"x": 121000, "y": 487000},
                "example_wgs84": {"lat": 52.3676, "lon": 4.9041}
            }
        
        result["source"] = "pyproj coordinate transformation"
        return result
        
    except ImportError:
        return {
            "error": "pyproj library not installed. Run: pip install pyproj",
            "fallback": "Approximate conversion: RD to WGS84 requires pyproj"
        }
    except Exception as e:
        return {
            "error": f"Coordinate conversion failed: {str(e)}",
            "input": {"x": x, "y": y, "lat": lat, "lon": lon}
        }

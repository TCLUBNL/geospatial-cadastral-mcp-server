import requests
from typing import Dict, Any

def get_3d_building_data(x: float, y: float, radius: int = 100) -> Dict[str, Any]:
    """
    Fetch 3D building height and elevation data from 3D Basisvoorziening.
    
    Args:
        x: RD X-coordinate (EPSG:28992)
        y: RD Y-coordinate (EPSG:28992)
        radius: Search radius in meters (default 100)
    
    Returns:
        Dictionary containing 3D building geometries and height information
    """
    base_url = "https://service.pdok.nl/lv/3d-basisvoorziening/wfs/v1_0"
    
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": "basisvoorziening:lod12",
        "outputFormat": "json",
        "srsName": "EPSG:28992",
        "count": 50,
        "CQL_FILTER": f"DWithin(geometrie, POINT({x} {y}), {radius}, meters)"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        features = data.get("features", [])
        
        results = []
        for feature in features:
            props = feature.get("properties", {})
            geom = feature.get("geometry", {})
            
            results.append({
                "building_id": props.get("gml_id"),
                "height_ground": props.get("h_maaiveld"),
                "height_roof": props.get("h_dak_max"),
                "height_relative": props.get("relatievehoogte"),
                "lod_level": props.get("lod"),
                "geometry_type": geom.get("type"),
                "coordinates": geom.get("coordinates")
            })
        
        return {
            "query_location": {"x": x, "y": y},
            "radius_m": radius,
            "buildings_found": len(results),
            "results": results,
            "source": "PDOK 3D Basisvoorziening WFS v1.0"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch 3D building data: {str(e)}",
            "query_location": {"x": x, "y": y}
        }

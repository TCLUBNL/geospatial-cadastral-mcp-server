import requests
from typing import Dict, Any

def get_topography(x: float, y: float, radius: int = 500, layer: str = "bgt") -> Dict[str, Any]:
    """
    Fetch topographical features from BGT (large-scale) or BRT/TOP10NL (base maps).
    
    Args:
        x: RD X-coordinate (EPSG:28992)
        y: RD Y-coordinate (EPSG:28992)
        radius: Search radius in meters
        layer: 'bgt' for large-scale or 'top10nl' for base maps
    
    Returns:
        Dictionary containing topographical features (roads, water, buildings, etc.)
    """
    if layer == "bgt":
        base_url = "https://service.pdok.nl/lv/bgt/wfs/v1_0"
        type_name = "bgt:bgt_all"
    else:  # top10nl
        base_url = "https://service.pdok.nl/brt/top10nl/wfs/v1_0"
        type_name = "top10nl:top10nl_all"
    
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": type_name,
        "outputFormat": "json",
        "srsName": "EPSG:28992",
        "count": 100,
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
                "feature_id": props.get("gml_id"),
                "feature_type": props.get("bronhouder") or props.get("typegebied"),
                "description": props.get("objecteindtijd"),
                "geometry_type": geom.get("type"),
                "coordinates": geom.get("coordinates")
            })
        
        return {
            "query_location": {"x": x, "y": y},
            "radius_m": radius,
            "layer": layer.upper(),
            "features_found": len(results),
            "results": results,
            "source": f"PDOK {layer.upper()} WFS v1.0"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch topography data: {str(e)}",
            "query_location": {"x": x, "y": y},
            "layer": layer
        }

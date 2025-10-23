import requests
from typing import Dict, Any

def get_noise_data(x: float, y: float, noise_type: str = "wegverkeerslawaai") -> Dict[str, Any]:
    """
    Fetch 3D noise modeling data for traffic and industrial noise.
    
    Args:
        x: RD X-coordinate (EPSG:28992)
        y: RD Y-coordinate (EPSG:28992)
        noise_type: Type of noise ('wegverkeerslawaai', 'railverkeerslawaai', 'industrielawaai')
    
    Returns:
        Dictionary containing noise levels in dB at the specified location
    """
    base_url = "https://service.pdok.nl/rvo/geluid3d/wfs/v1_0"
    
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": f"geluid3d:{noise_type}",
        "outputFormat": "json",
        "srsName": "EPSG:28992",
        "count": 10,
        "CQL_FILTER": f"INTERSECTS(geometrie, POINT({x} {y}))"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        features = data.get("features", [])
        
        results = []
        for feature in features:
            props = feature.get("properties", {})
            
            results.append({
                "noise_type": noise_type,
                "noise_level_lden": props.get("lden"),
                "noise_level_lnight": props.get("lnight"),
                "year": props.get("jaar"),
                "source_description": props.get("omschrijving"),
                "zone_type": props.get("zonetype")
            })
        
        return {
            "query_location": {"x": x, "y": y},
            "noise_type": noise_type,
            "results": results,
            "count": len(results),
            "source": "PDOK 3D Geluid WFS v1.0",
            "note": "Noise levels in dB - Lden (day-evening-night), Lnight (night only)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch noise data: {str(e)}",
            "query_location": {"x": x, "y": y},
            "noise_type": noise_type
        }

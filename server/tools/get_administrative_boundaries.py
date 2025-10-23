import requests
from typing import Dict, Any, Optional

def get_administrative_boundaries(admin_type: str = "gemeente", 
                                  name: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch administrative boundaries for municipalities, provinces, or other regions.
    
    Args:
        admin_type: Type of boundary ('gemeente', 'provincie', 'waterschap')
        name: Optional name filter (e.g., 'Amsterdam')
    
    Returns:
        Dictionary containing boundary geometries and metadata
    """
    base_url = "https://service.pdok.nl/kadaster/bestuurlijkegebieden/wfs/v1_0"
    
    type_mapping = {
        "gemeente": "bestuurlijkegebieden:gemeenten",
        "provincie": "bestuurlijkegebieden:provincies",
        "waterschap": "bestuurlijkegebieden:waterschappen"
    }
    
    type_name = type_mapping.get(admin_type, type_mapping["gemeente"])
    
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": type_name,
        "outputFormat": "json",
        "count": 50
    }
    
    if name:
        params["CQL_FILTER"] = f"naam ILIKE '%{name}%'"
    
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
                "code": props.get("code"),
                "name": props.get("naam"),
                "type": admin_type,
                "province": props.get("provincienaam"),
                "geometry_type": geom.get("type"),
                "coordinates": geom.get("coordinates"),
                "bbox": feature.get("bbox")
            })
        
        return {
            "admin_type": admin_type,
            "name_filter": name,
            "results": results,
            "count": len(results),
            "source": "PDOK Bestuurlijke Gebieden WFS v1.0"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch administrative boundaries: {str(e)}",
            "admin_type": admin_type
        }

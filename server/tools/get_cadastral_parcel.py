import requests
from typing import Dict, Any, Optional

def get_cadastral_parcel(parcel_id: Optional[str] = None, 
                         x: Optional[float] = None, 
                         y: Optional[float] = None) -> Dict[str, Any]:
    """
    Fetch cadastral parcel data including boundaries, ownership info, and parcel numbers.
    
    Args:
        parcel_id: Cadastral parcel identifier (e.g., "ASD01-A-1234")
        x: RD X-coordinate (optional, for point-in-parcel lookup)
        y: RD Y-coordinate (optional, for point-in-parcel lookup)
    
    Returns:
        Dictionary containing parcel boundaries, area, municipality, section
    """
    base_url = "https://service.pdok.nl/kadaster/kadastralekaart/wfs/v5_0"
    
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": "kadastralekaart:kadastralegrens",
        "outputFormat": "json",
        "count": 10
    }
    
    if parcel_id:
        params["CQL_FILTER"] = f"identificatie='{parcel_id}'"
    elif x and y:
        params["CQL_FILTER"] = f"INTERSECTS(geometrie, POINT({x} {y}))"
    else:
        return {"error": "Either parcel_id or (x, y) coordinates required"}
    
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
                "parcel_id": props.get("identificatie"),
                "municipality": props.get("gemeentenaam"),
                "section": props.get("sectie"),
                "parcel_number": props.get("perceelnummer"),
                "geometry_type": geom.get("type"),
                "coordinates": geom.get("coordinates"),
                "area_m2": props.get("oppervlakte"),
                "cadastral_designation": props.get("kadastraleaanduiding")
            })
        
        return {
            "parcel_id": parcel_id,
            "query_coords": {"x": x, "y": y} if x and y else None,
            "results": results,
            "count": len(results),
            "source": "PDOK Kadastrale Kaart WFS v5.0"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch cadastral data: {str(e)}",
            "parcel_id": parcel_id
        }

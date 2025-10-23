import requests
from typing import Dict, Any, Optional

def search_location(query: str, filter_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for addresses, cadastral parcels, or locations using PDOK Location Server.
    
    Args:
        query: Search query (address, postal code, parcel ID, or place name)
        filter_type: Optional filter ('adres', 'perceel', 'postcode', 'gemeente', 'woonplaats')
    
    Returns:
        Dictionary containing search results with coordinates and identifiers
    """
    base_url = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/free"
    
    params = {
        "q": query,
        "rows": 20
    }
    
    if filter_type:
        params["fq"] = f"type:{filter_type}"
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for doc in data.get("response", {}).get("docs", []):
            results.append({
                "id": doc.get("id"),
                "type": doc.get("type"),
                "display_name": doc.get("weergavenaam"),
                "street": doc.get("straatnaam"),
                "house_number": doc.get("huis_nlt"),
                "postal_code": doc.get("postcode"),
                "city": doc.get("woonplaatsnaam"),
                "municipality": doc.get("gemeentenaam"),
                "province": doc.get("provincienaam"),
                "centroid_rd": {
                    "x": doc.get("centroide_rd"),
                    "y": doc.get("centroide_rd") 
                },
                "centroid_ll": {
                    "lat": doc.get("centroide_ll", "").split()[0] if doc.get("centroide_ll") else None,
                    "lon": doc.get("centroide_ll", "").split()[1] if doc.get("centroide_ll") else None
                },
                "score": doc.get("score")
            })
        
        return {
            "query": query,
            "filter": filter_type,
            "num_found": data.get("response", {}).get("numFound", 0),
            "results": results,
            "source": "PDOK Location Server v3.1"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to search location: {str(e)}",
            "query": query
        }

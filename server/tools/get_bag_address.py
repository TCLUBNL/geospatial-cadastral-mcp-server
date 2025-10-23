import requests
from typing import Dict, Any, Optional

def get_bag_address(bag_id: Optional[str] = None, postal_code: Optional[str] = None, 
                    house_number: Optional[int] = None) -> Dict[str, Any]:
    """
    Fetch detailed building and address data from BAG (Basisregistratie Adressen en Gebouwen).
    
    Args:
        bag_id: BAG identifier (if known)
        postal_code: Postal code (e.g., "1012JS")
        house_number: House number
    
    Returns:
        Dictionary containing building details, construction year, surface area, usage
    """
    base_url = "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adressen"
    
    params = {}
    if bag_id:
        url = f"{base_url}/{bag_id}"
    elif postal_code and house_number:
        params["postcode"] = postal_code
        params["huisnummer"] = house_number
        url = base_url
    else:
        return {"error": "Either bag_id or (postal_code + house_number) required"}
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # BAG API returns detailed structured data
        results = data.get("_embedded", {}).get("adressen", [])
        
        formatted_results = []
        for item in results:
            formatted_results.append({
                "bag_id": item.get("identificatie"),
                "street": item.get("openbareRuimteNaam"),
                "house_number": item.get("huisnummer"),
                "postal_code": item.get("postcode"),
                "city": item.get("woonplaatsNaam"),
                "status": item.get("status"),
                "coordinates": item.get("geolocatie", {}).get("punt", {}),
                "construction_year": item.get("oorspronkelijkBouwjaar"),
                "surface_area": item.get("oppervlakte"),
                "usage": item.get("gebruiksdoel")
            })
        
        return {
            "postal_code": postal_code,
            "house_number": house_number,
            "bag_id": bag_id,
            "results": formatted_results,
            "count": len(formatted_results),
            "source": "BAG Kadaster API v2"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch BAG data: {str(e)}",
            "postal_code": postal_code,
            "house_number": house_number
        }

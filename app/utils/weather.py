"""
Weather Service (Open-Meteo)

Provides real-time atmospheric data from Open-Meteo API.
No API key required.
"""

import math
import requests
from typing import Dict

def get_mock_weather(lat: float, lon: float) -> Dict[str, any]:
    """
    Get REAL weather data from Open-Meteo based on latitude and longitude.
    
    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
    
    Returns:
        Dict with weather parameters:
        - wind_speed (m/s)
        - ambient_temperature (K)
        - stability_class (A-F)
    """
    # Validate coordinates
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    
    try:
        # Use Open-Meteo for real data
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&wind_speed_unit=ms"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data["current"]
        temp_c = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]
        
        # Determine stability class roughly based on wind and temp (simplified)
        stability_class = "D"
        if wind_speed < 2 and temp_c > 25:
            stability_class = "A"
        elif wind_speed < 3 and temp_c > 20:
            stability_class = "B"
        elif wind_speed < 5:
            stability_class = "C"
            
        return {
            "wind_speed": round(wind_speed, 1),
            "ambient_temperature": round(temp_c + 273.15, 1),
            "stability_class": stability_class,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "note": "Real-time atmospheric data from Open-Meteo"
        }
    except Exception as e:
        # Fallback to a simplified climate model if API is down
        base_temp_c = 25 - abs(lat) * 0.5
        ambient_temperature = base_temp_c + 273.15
        
        abs_lat = abs(lat)
        if abs_lat < 30:
            wind_speed = 3.0
            stability_class = "B"
        else:
            wind_speed = 5.0
            stability_class = "D"
            
        return {
            "wind_speed": round(wind_speed, 1),
            "ambient_temperature": round(ambient_temperature, 1),
            "stability_class": stability_class,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "note": f"Weather data estimated (API error: {str(e)})"
        }

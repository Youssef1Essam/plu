import os
import requests
from typing import Dict, Any

def get_egypt_weather(city_name: str) -> Dict[str, Any]:
    """
    Fetch real weather data from Open-Meteo for any city.
    No API key required.
    """
    try:
        # 1. Geocoding API to get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        geo_res = requests.get(geo_url, timeout=10)
        geo_res.raise_for_status()
        geo_data = geo_res.json()
        
        if not geo_data.get("results"):
            raise ValueError(f"City '{city_name}' not found.")
            
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        full_city_name = location.get("name", city_name)
        country = location.get("country", "")
        
        display_name = f"{full_city_name}, {country}" if country else full_city_name
        
        # 2. Weather API to get current conditions
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&wind_speed_unit=ms"
        weather_res = requests.get(weather_url, timeout=10)
        weather_res.raise_for_status()
        weather_data = weather_res.json()
        
        current = weather_data["current"]
        temp_c = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]
        
        # Determine Pasquill-Gifford stability class from wind speed and temperature.
        # Low wind + high temp = stagnant/stable atmosphere (Class E or F) — HIGH RISK in Cairo summers.
        # High wind = neutral or unstable (Class C or D) — better dispersion.
        if wind_speed < 2:
            stability_class = "F"   # Very stable / stagnant — worst case
        elif wind_speed < 3:
            stability_class = "E"   # Slightly stable
        elif wind_speed < 5:
            stability_class = "D"   # Neutral
        elif wind_speed < 8 and temp_c > 25:
            stability_class = "C"   # Slightly unstable (hot + breezy)
        elif wind_speed >= 8:
            stability_class = "B"   # Unstable — good dispersion
        else:
            stability_class = "D"   # Default neutral

        return {
            "wind_speed": max(wind_speed, 0.5),  # Prevent division by zero in physics
            "ambient_temperature": temp_c + 273.15,
            "stability_class": stability_class,
            "city": display_name,
            "note": f"Real-time data from Open-Meteo | Wind: {wind_speed:.1f} m/s, Temp: {temp_c:.1f}°C"
        }
    except Exception as e:
        # Fallback to defaults if API fails
        return {
            "wind_speed": 4.5,
            "ambient_temperature": 298.15,
            "stability_class": "C",
            "city": city_name,
            "note": f"Weather data estimated (Network: {str(e)})"
        }

def determine_scenario_for_egypt_city(city_name: str) -> str:
    """
    Industrial cities like Helwan, Shubra El-Kheima get 'factory'
    Others get 'waste_burning' or 'power_plant'
    """
    city_lower = city_name.lower()
    industrial_cities = ["helwan", "حلوان", "shubra", "شبرا", "ramadan", "رمضان", "sadat", "السادات", "obour", "العبور", "suez", "السويس", "10th", "العاشر"]
    
    for ind in industrial_cities:
        if ind in city_lower:
            return "factory"
            
    if "power" in city_lower or "كهرباء" in city_lower:
        return "power_plant"
        
    return "waste_burning"

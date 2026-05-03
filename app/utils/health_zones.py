from typing import List, Dict

def calculate_health_zones(peak_concentration: float, impact_distance: float) -> List[Dict]:
    """
    Calculate health zones dynamically based on peak concentration and impact distance.
    WHO thresholds:
    - > 0.01: danger for everyone
    - > 0.001: danger for asthma, heart disease, elderly, children
    - > 0.0001: caution for asthma and children only
    - < 0.0001: generally safe
    """
    if impact_distance <= 0 or peak_concentration < 0.0001:
        return [{
            "zone_name": "Safe Zone",
            "distance_range": "0+ meters",
            "color_code": "green",
            "pollutants": ["None or trace amounts"],
            "vulnerable_groups": ["None"],
            "warning_english": "Area is generally safe for all groups.",
            "warning_arabic": "المنطقة آمنة عموماً لجميع الفئات."
        }]
    
    zones = []
    current_conc = peak_concentration
    
    steps = 0
    if peak_concentration > 0.01:
        steps = 3
    elif peak_concentration > 0.001:
        steps = 2
    else:
        steps = 1
        
    distances = [0]
    for i in range(1, steps + 1):
        distances.append(int(impact_distance * (i / steps)))
        
    for i in range(steps):
        start_m = distances[i]
        end_m = distances[i+1]
        
        band_conc = current_conc
        if band_conc > 0.01:
            zones.append({
                "zone_name": "Danger Zone",
                "distance_range": f"{start_m}-{end_m}m",
                "color_code": "red",
                "pollutants": ["SO2", "NO2", "PM2.5"],
                "vulnerable_groups": ["Everyone", "Asthma patients", "Heart disease", "Children under 12", "Elderly"],
                "warning_english": "Critical danger. Everyone should avoid this area.",
                "warning_arabic": "خطر حرج. يجب على الجميع تجنب هذه المنطقة."
            })
        elif band_conc > 0.001:
            zones.append({
                "zone_name": "High Risk Zone",
                "distance_range": f"{start_m}-{end_m}m",
                "color_code": "orange",
                "pollutants": ["SO2", "NO2", "PM2.5"],
                "vulnerable_groups": ["Asthma patients", "Heart disease", "Elderly", "Children under 12"],
                "warning_english": "High risk. Vulnerable groups must evacuate or stay indoors.",
                "warning_arabic": "عالي الخطورة. يجب على الفئات الضعيفة الإخلاء أو البقاء في الداخل."
            })
        elif band_conc >= 0.0001:
            zones.append({
                "zone_name": "Caution Zone",
                "distance_range": f"{start_m}-{end_m}m",
                "color_code": "yellow",
                "pollutants": ["SO2", "NO2", "PM2.5"],
                "vulnerable_groups": ["Asthma patients", "Children under 12"],
                "warning_english": "Caution. Asthma patients and children should limit outdoor activities.",
                "warning_arabic": "تنبيه. يجب على مرضى الربو والأطفال تقليل الأنشطة الخارجية."
            })
        
        current_conc *= 0.1
        
    zones.append({
        "zone_name": "Safe Zone",
        "distance_range": f">{distances[-1]}m",
        "color_code": "green",
        "pollutants": ["None or trace amounts"],
        "vulnerable_groups": ["None"],
        "warning_english": "Area is generally safe for all groups.",
        "warning_arabic": "المنطقة آمنة عموماً لجميع الفئات."
    })
    
    merged = []
    for z in zones:
        if not merged or merged[-1]["zone_name"] != z["zone_name"]:
            merged.append(z)
        else:
            prev = merged[-1]["distance_range"]
            curr = z["distance_range"]
            if prev.startswith(">"): continue
            
            start = prev.split("-")[0]
            if curr.startswith(">"):
                merged[-1]["distance_range"] = f">{start}m"
            else:
                end = curr.split("-")[1]
                merged[-1]["distance_range"] = f"{start}-{end}"
                
    return merged

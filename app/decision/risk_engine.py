"""
Risk Decision Engine

Combines concentration and impact distance to produce actionable risk assessments.
This is the core decision logic that transforms physics into product value.
"""

from app.utils.constants import (
    THRESHOLD_LOW, 
    THRESHOLD_MEDIUM, 
    DISTANCE_SHORT, 
    DISTANCE_MEDIUM
)


def determine_risk_level(concentration: float, impact_distance: float) -> str:
    """
    Determine risk level based on BOTH concentration and impact distance.
    
    Logic:
    - HIGH: High concentration OR long spread distance
    - MEDIUM: Moderate concentration OR medium spread distance  
    - LOW: Low concentration AND short distance (or negligible impact)
    
    Args:
        concentration: Peak concentration (g/m³)
        impact_distance: Distance where concentration drops below threshold (m)
                        0 means concentration never exceeded threshold (negligible)
    
    Returns:
        str: "LOW", "MEDIUM", or "HIGH"
    """
    # HIGH RISK: Either high concentration OR long-range impact
    if concentration >= THRESHOLD_MEDIUM or impact_distance > DISTANCE_MEDIUM:
        return "HIGH"
    
    # MEDIUM RISK: Either moderate concentration OR medium-range impact
    elif concentration >= THRESHOLD_LOW or impact_distance > DISTANCE_SHORT:
        return "MEDIUM"
    
    # LOW RISK: Low concentration AND short/no distance
    else:
        return "LOW"


def generate_explanation(
    risk_level: str,
    concentration: float,
    impact_distance: float,
    wind_speed: float,
    stability_class: str,
    effective_height: float
) -> str:
    """
    Generate scientifically accurate explanation for the risk assessment.
    
    Uses actual physics parameters to explain WHY this risk level was assigned.
    NO hallucination - only use provided data.
    """
    explanations = []
    
    # Risk level statement
    explanations.append(f"{risk_level.capitalize()} risk detected.")
    
    # Concentration analysis
    if concentration >= THRESHOLD_MEDIUM:
        explanations.append(
            f"Peak concentration of {concentration:.2e} g/m³ exceeds medium threshold."
        )
    elif concentration >= THRESHOLD_LOW:
        explanations.append(
            f"Moderate concentration of {concentration:.2e} g/m³ detected."
        )
    else:
        explanations.append(
            f"Low concentration of {concentration:.2e} g/m³ detected."
        )
    
    # Impact distance analysis
    if impact_distance == 0:
        explanations.append(
            "Negligible ground-level impact - concentrations remain below threshold at all distances."
        )
    elif impact_distance > DISTANCE_MEDIUM:
        explanations.append(
            f"Pollutants spread over {impact_distance:.0f} meters, indicating long-range impact."
        )
    elif impact_distance > DISTANCE_SHORT:
        explanations.append(
            f"Pollutants spread over {impact_distance:.0f} meters, indicating medium-range impact."
        )
    else:
        explanations.append(
            f"Impact limited to {impact_distance:.0f} meters from source."
        )
    
    # Atmospheric conditions
    stability_descriptions = {
        "A": "very unstable atmospheric conditions (Class A) promote rapid vertical mixing",
        "B": "unstable atmospheric conditions (Class B) promote good vertical mixing",
        "C": "slightly unstable atmospheric conditions (Class C) allow moderate dispersion",
        "D": "neutral atmospheric conditions (Class D) provide average dispersion",
        "E": "slightly stable atmospheric conditions (Class E) limit vertical mixing",
        "F": "very stable atmospheric conditions (Class F) severely limit dispersion"
    }
    
    explanations.append(stability_descriptions.get(stability_class, f"Stability class {stability_class} conditions"))
    
    # Wind speed analysis
    if wind_speed < 2.0:
        explanations.append(
            f"Low wind speed ({wind_speed:.1f} m/s) reduces horizontal dispersion, causing pollutants to accumulate."
        )
    elif wind_speed > 8.0:
        explanations.append(
            f"High wind speed ({wind_speed:.1f} m/s) enhances horizontal dispersion."
        )
    else:
        explanations.append(
            f"Moderate wind speed ({wind_speed:.1f} m/s) provides typical dispersion."
        )
    
    # Plume rise analysis
    if effective_height > 200:
        explanations.append(
            f"High effective plume height ({effective_height:.1f} m) reduces ground-level concentrations near source."
        )
    elif effective_height < 50:
        explanations.append(
            f"Low effective plume height ({effective_height:.1f} m) may increase ground-level concentrations."
        )
    
    return " ".join(explanations)


def generate_recommendation(risk_level: str, location_type: str) -> str:
    """
    Generate actionable recommendations based on risk level and location context.
    
    Args:
        risk_level: "LOW", "MEDIUM", or "HIGH"
        location_type: "industrial", "urban", or "rural"
    
    Returns:
        str: Actionable recommendation
    """
    recommendations = {
        "LOW": {
            "industrial": "Minimal impact. Safe under normal operating conditions. Continue routine monitoring.",
            "urban": "Minimal impact on populated areas. Safe under current conditions.",
            "rural": "Minimal environmental impact. Safe under normal conditions."
        },
        "MEDIUM": {
            "industrial": "Monitor air quality continuously. Ensure workers in affected areas use appropriate PPE. Consider reducing emission rates during unfavorable conditions.",
            "urban": "Monitor air quality in nearby residential areas. Avoid prolonged outdoor exposure in downwind zones. Consider public health advisories if conditions persist.",
            "rural": "Monitor environmental impact on vegetation and wildlife. Avoid prolonged exposure in affected areas."
        },
        "HIGH": {
            "industrial": "IMMEDIATE ACTION REQUIRED. Potential health risk to workers and nearby populations. Implement emission reduction measures immediately. Evacuate non-essential personnel from downwind areas. Notify regulatory authorities.",
            "urban": "CRITICAL RISK. Avoid affected areas immediately. Issue public health warnings. Implement emergency emission controls. Consider temporary facility shutdown if conditions persist.",
            "rural": "HIGH ENVIRONMENTAL RISK. Significant impact on air quality. Avoid affected areas. Implement immediate emission reduction. Monitor ecological impact."
        }
    }
    
    return recommendations.get(risk_level, {}).get(
        location_type, 
        f"{risk_level} risk detected. Take appropriate precautions."
    )

"""
Warning Generation

Generates warnings for conditions that may affect model accuracy or indicate concerns.
"""

from typing import List


def generate_warnings(
    wind_speed: float,
    stability_class: str,
    concentration: float,
    impact_distance: float,
    stack_height: float,
    effective_height: float
) -> List[str]:
    """
    Generate warnings based on input conditions and results.
    
    Args:
        wind_speed: Wind speed (m/s)
        stability_class: Atmospheric stability class (A-F)
        concentration: Peak concentration (g/m³)
        impact_distance: Impact distance (m)
        stack_height: Physical stack height (m)
        effective_height: Effective stack height (m)
    
    Returns:
        List of warning strings
    """
    warnings = []
    
    # Wind speed warnings
    if wind_speed < 1.0:
        warnings.append(
            "Very low wind speed (< 1 m/s) may reduce model accuracy. "
            "Gaussian plume model is less reliable under calm conditions."
        )
    elif wind_speed < 0.5:
        warnings.append(
            "Wind speed below minimum threshold (0.5 m/s). "
            "Model results may not be valid."
        )
    
    if wind_speed > 15.0:
        warnings.append(
            "Very high wind speed (> 15 m/s) may introduce turbulence effects "
            "not fully captured by the model."
        )
    
    # Stability class warnings
    if stability_class.upper() == "F":
        warnings.append(
            "Very stable atmospheric conditions (Class F) can cause pollutants to "
            "accumulate near ground level with minimal dispersion. "
            "Monitor air quality closely."
        )
    
    if stability_class.upper() == "A":
        warnings.append(
            "Very unstable atmospheric conditions (Class A) create high variability. "
            "Actual concentrations may fluctuate significantly."
        )
    
    # Concentration warnings
    if concentration >= 0.001:
        warnings.append(
            "Very high concentration detected (≥ 0.001 g/m³). "
            "Immediate action recommended to reduce emissions or evacuate affected areas."
        )
    
    if concentration >= 0.01:
        warnings.append(
            "CRITICAL: Extremely high concentration (≥ 0.01 g/m³). "
            "Severe health risk. Emergency response required."
        )
    
    # Impact distance warnings
    if impact_distance >= 5000:
        warnings.append(
            "Impact distance reaches maximum simulation range (5000m). "
            "Actual impact may extend further. Consider extended analysis."
        )
    
    # Stack height warnings
    if stack_height < 20:
        warnings.append(
            "Low stack height (< 20m) may result in high ground-level concentrations "
            "near the source. Consider stack height increase for better dispersion."
        )
    
    # Plume rise warnings
    plume_rise = effective_height - stack_height
    if plume_rise < 5:
        warnings.append(
            "Low plume rise (< 5m) indicates insufficient buoyancy. "
            "Consider increasing stack temperature or exit velocity."
        )
    
    if plume_rise > 200:
        warnings.append(
            "Very high plume rise (> 200m) detected. "
            "Verify stack parameters are realistic."
        )
    
    return warnings

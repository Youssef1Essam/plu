"""
Confidence Score Calculation

Estimates model confidence based on atmospheric conditions.
Higher confidence when conditions are well-suited for Gaussian plume modeling.
"""


def calculate_confidence(
    wind_speed: float,
    stability_class: str,
    concentration: float
) -> float:
    """
    Calculate confidence score (0 to 1) for the risk assessment.
    
    Higher confidence when:
    - Low wind speed (less turbulence variability)
    - Stable atmospheric conditions (E, F)
    - Moderate concentration values (not extreme)
    
    Lower confidence when:
    - Very unstable conditions (A, B)
    - Very high or very low wind speeds
    - Extreme concentration values
    
    Args:
        wind_speed: Wind speed (m/s)
        stability_class: Atmospheric stability class (A-F)
        concentration: Peak concentration (g/m³)
    
    Returns:
        float: Confidence score between 0 and 1
    """
    confidence = 1.0
    
    # Stability class factor
    # Stable conditions (E, F) → higher confidence
    # Unstable conditions (A, B) → lower confidence
    stability_factors = {
        "A": 0.70,  # Very unstable - high variability
        "B": 0.80,  # Unstable - moderate variability
        "C": 0.90,  # Slightly unstable
        "D": 0.95,  # Neutral - most predictable
        "E": 0.98,  # Slightly stable - very predictable
        "F": 1.00   # Very stable - most predictable
    }
    confidence *= stability_factors.get(stability_class.upper(), 0.85)
    
    # Wind speed factor
    # Very low wind (< 1 m/s) → lower confidence (model validity concern)
    # Very high wind (> 15 m/s) → lower confidence (turbulence)
    # Moderate wind (2-8 m/s) → higher confidence
    if wind_speed < 1.0:
        confidence *= 0.70  # Model validity concern
    elif wind_speed < 2.0:
        confidence *= 0.85
    elif wind_speed <= 8.0:
        confidence *= 1.00  # Optimal range
    elif wind_speed <= 15.0:
        confidence *= 0.90
    else:
        confidence *= 0.75  # High turbulence
    
    # Concentration factor
    # Extreme values → lower confidence
    if concentration > 0.01:  # Very high concentration
        confidence *= 0.85
    elif concentration < 1e-10:  # Negligible concentration
        confidence *= 0.90
    
    # Ensure confidence stays in [0, 1]
    return max(0.0, min(1.0, confidence))

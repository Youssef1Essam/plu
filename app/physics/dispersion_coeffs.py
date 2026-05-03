from app.utils.constants import ALPHA_MAP

def compute_sigma_y(stability_class: str, x: float) -> float:
    """
    Compute crosswind dispersion coefficient (σy).
    σy = α * x / (1 + 0.0001 * x)
    """
    alpha = ALPHA_MAP.get(stability_class.upper())
    if alpha is None:
        raise ValueError(f"Invalid stability class: {stability_class}")
    
    return (alpha * x) / (1 + 0.0001 * x)

def compute_sigma_z(stability_class: str, x: float) -> float:
    """
    Compute vertical dispersion coefficient (σz).
    """
    sc = stability_class.upper()
    if sc == "A":
        return 0.2 * x
    elif sc == "B":
        return 0.12 * x
    elif sc == "C":
        return (0.08 * x) / (1 + 0.0002 * x)
    elif sc == "D":
        return (0.06 * x) / (1 + 0.0015 * x)
    elif sc == "E":
        return (0.03 * x) / (1 + 0.0003 * x)
    elif sc == "F":
        return (0.016 * x) / (1 + 0.0003 * x)
    else:
        raise ValueError(f"Invalid stability class: {stability_class}")

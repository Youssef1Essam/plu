from app.utils.constants import GRAVITY

def compute_buoyancy_flux(ve: float, d: float, ts: float, ta: float) -> float:
    """
    Compute buoyancy flux (Fb) using Briggs formula.
    Fb = (g * ve * d^2 * (Ts - Ta)) / (4 * Ts)
    """
    return (GRAVITY * ve * (d**2) * (ts - ta)) / (4 * ts)

def compute_plume_rise(fb: float, u: float) -> float:
    """
    Compute plume rise (Δh).
    Δh = Fb / wind_speed
    Note: wind_speed (u) must be > 0.
    """
    return fb / u

def compute_effective_height(hs: float, delta_h: float) -> float:
    """
    Compute effective stack height (H).
    H = stack_height + Δh
    """
    return hs + delta_h

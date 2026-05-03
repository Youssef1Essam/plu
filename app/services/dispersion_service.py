from app.models.request import PredictRequest
from app.models.response import PredictResponse
from app.physics.plume_rise import compute_buoyancy_flux, compute_plume_rise, compute_effective_height
from app.physics.dispersion_coeffs import compute_sigma_y, compute_sigma_z
from app.physics.concentration import compute_concentration
from app.utils.risk import classify_risk, build_notes

def process_prediction(data: PredictRequest) -> PredictResponse:
    """
    Orchestrate the dispersion calculation and risk analysis.
    """
    # 1. Plume Rise Calculations
    fb = compute_buoyancy_flux(
        data.exit_velocity, 
        data.stack_diameter, 
        data.stack_temperature, 
        data.ambient_temperature
    )
    delta_h = compute_plume_rise(fb, data.wind_speed)
    h_eff = compute_effective_height(data.stack_height, delta_h)
    
    # 2. Dispersion Coefficients
    sy = compute_sigma_y(data.stability_class, data.x)
    sz = compute_sigma_z(data.stability_class, data.x)
    
    # 3. Concentration
    conc = compute_concentration(
        data.emission_rate, 
        data.wind_speed, 
        sy, 
        sz, 
        data.y, 
        data.z, 
        h_eff
    )
    
    # 4. Risk and Notes
    risk = classify_risk(conc)
    notes = build_notes(data.stability_class, h_eff, data.x)
    
    return PredictResponse(
        concentration=conc,
        effective_height=h_eff,
        sigma_y=sy,
        sigma_z=sz,
        risk_level=risk,
        notes=notes
    )

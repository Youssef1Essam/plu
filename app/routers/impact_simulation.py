"""
Impact Simulation Router

Endpoint: /simulate-impact
Provides detailed spread distance analysis with concentration profile.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.models.request import RiskAssessmentRequest
from app.physics.plume_rise import (
    compute_buoyancy_flux,
    compute_plume_rise,
    compute_effective_height
)
from app.physics.dispersion_coeffs import compute_sigma_y, compute_sigma_z
from app.physics.concentration import compute_concentration
from app.utils.constants import IMPACT_DISTANCE_MAX, IMPACT_DISTANCE_STEP, THRESHOLD_LOW

router = APIRouter()


class ConcentrationPoint(BaseModel):
    """Single point in concentration profile"""
    distance_meters: float
    concentration: float


class ImpactSimulationResponse(BaseModel):
    """Detailed impact spread analysis"""
    effective_height: float
    peak_concentration: float
    peak_distance_meters: float
    impact_distance_meters: float
    concentration_profile: List[ConcentrationPoint]


@router.post("/simulate-impact", response_model=ImpactSimulationResponse)
async def simulate_impact_spread(request: RiskAssessmentRequest):
    """
    Simulate Emission Impact Spread
    
    Computes concentration profile along downwind axis to show
    how far and how intensely pollution spreads.
    
    Returns:
    - Effective plume height
    - Peak concentration and location
    - Impact distance (where concentration drops below threshold)
    - Full concentration profile for visualization
    """
    try:
        # Step 1: Plume Rise
        fb = compute_buoyancy_flux(
            request.exit_velocity,
            request.stack_diameter,
            request.stack_temperature,
            request.ambient_temperature
        )
        delta_h = compute_plume_rise(fb, request.wind_speed)
        h_eff = compute_effective_height(request.stack_height, delta_h)
        
        # Step 2: Simulate concentration profile
        concentration_profile = []
        peak_concentration = 0.0
        peak_distance = 0.0
        impact_distance = 0.0
        
        x = IMPACT_DISTANCE_STEP
        while x <= IMPACT_DISTANCE_MAX:
            sy = compute_sigma_y(request.stability_class, x)
            sz = compute_sigma_z(request.stability_class, x)
            
            conc = compute_concentration(
                request.emission_rate,
                request.wind_speed,
                sy, sz,
                y=0.0, z=0.0,
                h=h_eff
            )
            
            concentration_profile.append(
                ConcentrationPoint(distance_meters=x, concentration=conc)
            )
            
            if conc > peak_concentration:
                peak_concentration = conc
                peak_distance = x
            
            if conc >= THRESHOLD_LOW:
                impact_distance = x
            elif impact_distance > 0:
                # Stop after dropping below threshold
                break
            
            x += IMPACT_DISTANCE_STEP
        
        return ImpactSimulationResponse(
            effective_height=h_eff,
            peak_concentration=peak_concentration,
            peak_distance_meters=peak_distance,
            impact_distance_meters=impact_distance,
            concentration_profile=concentration_profile
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Impact simulation failed: {str(e)}"
        )

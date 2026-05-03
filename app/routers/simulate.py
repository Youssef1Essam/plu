from fastapi import APIRouter, HTTPException
import numpy as np
from app.models.request import GridSimulateRequest, PredictRequest
from app.models.response import GridSimulateResponse, GridPoint
from app.services.dispersion_service import process_prediction
from app.physics.plume_rise import compute_buoyancy_flux, compute_plume_rise, compute_effective_height

router = APIRouter()

@router.post("/simulate-grid", response_model=GridSimulateResponse)
async def simulate_grid(request: GridSimulateRequest):
    """
    Simulate concentration over a 2D grid at a fixed height z.
    """
    try:
        # Pre-calculate effective height as it's constant for the grid
        fb = compute_buoyancy_flux(
            request.exit_velocity, 
            request.stack_diameter, 
            request.stack_temperature, 
            request.ambient_temperature
        )
        delta_h = compute_plume_rise(fb, request.wind_speed)
        h_eff = compute_effective_height(request.stack_height, delta_h)

        x_coords = np.linspace(request.x_min, request.x_max, request.x_steps)
        y_coords = np.linspace(request.y_min, request.y_max, request.y_steps)
        
        grid_results = []
        max_conc = -1.0
        peak_loc = {"x": 0.0, "y": 0.0, "z": request.z}

        for x in x_coords:
            for y in y_coords:
                # Reuse the service for each point
                point_req = PredictRequest(
                    emission_rate=request.emission_rate,
                    wind_speed=request.wind_speed,
                    stack_height=request.stack_height,
                    exit_velocity=request.exit_velocity,
                    stack_diameter=request.stack_diameter,
                    stack_temperature=request.stack_temperature,
                    ambient_temperature=request.ambient_temperature,
                    stability_class=request.stability_class,
                    x=float(x),
                    y=float(y),
                    z=request.z
                )
                res = process_prediction(point_req)
                
                grid_results.append(GridPoint(x=float(x), y=float(y), concentration=res.concentration))
                
                if res.concentration > max_conc:
                    max_conc = res.concentration
                    peak_loc = {"x": float(x), "y": float(y), "z": request.z}

        return GridSimulateResponse(
            grid=grid_results,
            peak_concentration=max_conc,
            peak_location=peak_loc,
            effective_height=h_eff
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

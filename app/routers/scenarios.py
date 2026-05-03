"""
Scenario-Based Risk Assessment Router

Endpoints for predefined scenarios and auto weather mode.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Literal

from app.models.request import RiskAssessmentRequest
from app.models.response import RiskAssessmentResponse
from app.services.risk_assessment_service import process_risk_assessment
from app.utils.scenarios import list_scenarios, get_scenario
from app.utils.weather import get_mock_weather

router = APIRouter()


class ScenarioListResponse(BaseModel):
    """Response for GET /scenarios"""
    scenarios: Dict[str, Dict[str, Any]]


class PredictScenarioRequest(BaseModel):
    """Request for POST /predict-scenario"""
    scenario: str = Field(..., description="Scenario name (power_plant, factory, waste_burning)")
    location_type: Literal["industrial", "urban", "rural"] = Field(
        "industrial",
        description="Location type for context-aware recommendations"
    )


class PredictAutoRequest(BaseModel):
    """Request for POST /predict-auto"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    scenario: str = Field(..., description="Scenario name (power_plant, factory, waste_burning)")
    location_type: Literal["industrial", "urban", "rural"] = Field(
        "industrial",
        description="Location type for context-aware recommendations"
    )


@router.get("/scenarios", response_model=ScenarioListResponse)
async def get_scenarios():
    """
    Get Predefined Scenarios
    
    Returns all available predefined emission scenarios with their parameters.
    Each scenario represents a realistic industrial emission source.
    
    Available scenarios:
    - **power_plant**: Large coal-fired power plant
    - **factory**: Medium-sized industrial facility
    - **waste_burning**: Waste incinerator
    """
    try:
        scenarios = list_scenarios()
        return ScenarioListResponse(scenarios=scenarios)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve scenarios: {str(e)}"
        )


@router.post("/predict-scenario", response_model=RiskAssessmentResponse)
async def predict_with_scenario(request: PredictScenarioRequest):
    """
    Risk Assessment with Predefined Scenario
    
    Runs risk assessment using a predefined emission scenario.
    Only requires scenario name and location type - all emission parameters
    are preset to realistic values.
    
    **Scenarios:**
    - `power_plant`: Large coal-fired power plant (high stack, high emissions)
    - `factory`: Industrial facility (medium stack, moderate emissions)
    - `waste_burning`: Waste incinerator (low stack, variable emissions)
    
    **Location Types:**
    - `industrial`: Focus on worker safety
    - `urban`: Focus on public health
    - `rural`: Focus on environmental impact
    """
    try:
        # Get scenario parameters
        scenario_params = get_scenario(request.scenario)
        
        # Create risk assessment request
        risk_request = RiskAssessmentRequest(
            emission_rate=scenario_params["emission_rate"],
            wind_speed=scenario_params["wind_speed"],
            stack_height=scenario_params["stack_height"],
            exit_velocity=scenario_params["exit_velocity"],
            stack_diameter=scenario_params["stack_diameter"],
            stack_temperature=scenario_params["stack_temperature"],
            ambient_temperature=scenario_params["ambient_temperature"],
            stability_class=scenario_params["stability_class"],
            location_type=request.location_type
        )
        
        # Process risk assessment
        return process_risk_assessment(risk_request)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Risk assessment failed: {str(e)}"
        )


@router.post("/predict-auto", response_model=RiskAssessmentResponse)
async def predict_with_auto_weather(request: PredictAutoRequest):
    """
    Risk Assessment with Auto Weather
    
    Runs risk assessment using a predefined scenario combined with
    mock weather data based on geographic location.
    
    **Note**: This uses mock weather data for demonstration.
    In production, integrate with a real weather API (OpenWeatherMap, NOAA, etc.)
    
    **Parameters:**
    - `lat`: Latitude (-90 to 90)
    - `lon`: Longitude (-180 to 180)
    - `scenario`: Emission scenario name
    - `location_type`: Context for recommendations
    
    **Weather Data:**
    Mock weather includes:
    - Wind speed (based on latitude patterns)
    - Ambient temperature (based on climate zones)
    - Stability class (based on location)
    """
    try:
        # Get scenario parameters
        scenario_params = get_scenario(request.scenario)
        
        # Get mock weather data
        weather = get_mock_weather(request.lat, request.lon)
        
        # Create risk assessment request
        # Use scenario parameters but override with weather data
        risk_request = RiskAssessmentRequest(
            emission_rate=scenario_params["emission_rate"],
            wind_speed=weather["wind_speed"],
            stack_height=scenario_params["stack_height"],
            exit_velocity=scenario_params["exit_velocity"],
            stack_diameter=scenario_params["stack_diameter"],
            stack_temperature=scenario_params["stack_temperature"],
            ambient_temperature=weather["ambient_temperature"],
            stability_class=weather["stability_class"],
            location_type=request.location_type
        )
        
        # Process risk assessment
        result = process_risk_assessment(risk_request)
        
        # Add weather note to warnings
        result.warnings.insert(0, weather["note"])
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Risk assessment failed: {str(e)}"
        )

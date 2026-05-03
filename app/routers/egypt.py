from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.models.response import RiskAssessmentResponse
from app.models.request import RiskAssessmentRequest
from app.utils.egypt_weather import get_egypt_weather, determine_scenario_for_egypt_city
from app.utils.scenarios import get_scenario
from app.services.risk_assessment_service import process_risk_assessment

router = APIRouter()

class EgyptPredictRequest(BaseModel):
    city_name: str = Field(..., description="Egypt city name in English or Arabic (e.g. Helwan, حلوان)")
    location_type: str = Field("industrial", description="Context for recommendations")

@router.post("/predict-egypt", response_model=RiskAssessmentResponse)
async def predict_egypt_city(request: EgyptPredictRequest):
    try:
        # 1. Fetch weather
        weather = get_egypt_weather(request.city_name)
        
        # 2. Determine scenario
        scenario_name = determine_scenario_for_egypt_city(request.city_name)
        scenario_params = get_scenario(scenario_name)
        
        # 3. Build risk request (override with weather)
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
        
        # 4. Process risk assessment
        result = process_risk_assessment(risk_request)
        
        # Add a warning note about the city and weather
        result.warnings.insert(0, f"Analysis for {weather['city']} using scenario: {scenario_name}. {weather['note']}")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Risk Assessment Router

Main product endpoint: /predict
Returns actionable risk assessments, not just raw numbers.
"""

from fastapi import APIRouter, HTTPException
from app.models.request import RiskAssessmentRequest
from app.models.response import RiskAssessmentResponse
from app.services.risk_assessment_service import process_risk_assessment

router = APIRouter()


@router.post("/predict", response_model=RiskAssessmentResponse)
async def assess_emission_risk(request: RiskAssessmentRequest):
    """
    Industrial Emission Risk Assessment
    
    Analyzes emission scenarios and provides actionable risk assessments
    based on Gaussian plume dispersion modeling.
    
    Returns:
    - Risk level (LOW/MEDIUM/HIGH)
    - Peak concentration
    - Impact distance (how far pollution spreads)
    - Scientific explanation
    - Actionable recommendations
    """
    try:
        return process_risk_assessment(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Risk assessment failed: {str(e)}"
        )

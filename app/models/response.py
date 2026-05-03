from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class HealthZone(BaseModel):
    zone_name: str
    distance_range: str
    color_code: str
    pollutants: List[str]
    vulnerable_groups: List[str]
    warning_english: str
    warning_arabic: str

class RiskAssessmentResponse(BaseModel):
    """Decision-focused risk assessment output"""
    risk_level: str
    peak_concentration: float
    impact_distance_meters: float
    effective_height: float
    explanation: str
    recommendation: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score (0-1)")
    warnings: List[str] = Field(default_factory=list, description="Warnings about conditions or results")
    ai_used: bool = Field(False, description="Whether an AI model was used for this assessment")
    health_zones: Optional[List[HealthZone]] = Field(None, description="Health impact zones with vulnerability analysis")
    
    # Audit and tracking (v2.3.0)
    assessment_id: str = Field(..., description="Unique tracking ID for this assessment")
    timestamp: str = Field(..., description="ISO timestamp of when the assessment was performed")
    
    # Advanced metrics (v2.2.0)
    impact_width_meters: Optional[float] = Field(None, description="Lateral spread width at peak distance (m)")
    time_to_impact_minutes: Optional[float] = Field(None, description="Time for pollutants to reach impact distance (min)")
    peak_distance_meters: Optional[float] = Field(None, description="Distance where concentration is maximum (m)")
    population_risk: Optional[str] = Field(None, description="Population risk assessment for urban areas")
    uncertainty_range: Optional[Dict[str, float]] = Field(None, description="Concentration uncertainty range")

class PredictResponse(BaseModel):
    concentration: float
    effective_height: float
    sigma_y: float
    sigma_z: float
    risk_level: str
    notes: str

class GridPoint(BaseModel):
    x: float
    y: float
    concentration: float

class GridSimulateResponse(BaseModel):
    grid: List[GridPoint]
    peak_concentration: float
    peak_location: Dict[str, float]
    effective_height: float

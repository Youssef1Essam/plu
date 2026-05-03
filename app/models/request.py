from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal
from app.utils.constants import STABILITY_CLASSES

class RiskAssessmentRequest(BaseModel):
    """Request for Industrial Emission Risk Assessment"""
    emission_rate: float = Field(..., gt=0, description="Emission rate Q (g/s)")
    wind_speed: float = Field(..., ge=0.5, description="Wind speed u (m/s)")
    stack_height: float = Field(..., gt=0, description="Stack height h (m)")
    exit_velocity: float = Field(..., gt=0, description="Exit velocity ve (m/s)")
    stack_diameter: float = Field(..., gt=0, description="Stack diameter d (m)")
    stack_temperature: float = Field(..., gt=0, description="Stack temperature Ts (K)")
    ambient_temperature: float = Field(..., gt=0, description="Ambient temperature Ta (K)")
    stability_class: str = Field(..., description="Atmospheric stability class (A-F)")
    location_type: Literal["industrial", "urban", "rural"] = Field(
        "industrial", 
        description="Location type for context-aware recommendations"
    )

    @field_validator("stability_class")
    @classmethod
    def validate_stability_class(cls, v: str) -> str:
        v = v.upper()
        if v not in STABILITY_CLASSES:
            raise ValueError(f"Invalid stability class. Must be one of: {', '.join(sorted(STABILITY_CLASSES))}")
        return v

    @model_validator(mode="after")
    def validate_temperatures(self) -> "RiskAssessmentRequest":
        if self.stack_temperature <= self.ambient_temperature:
            raise ValueError("Stack temperature must exceed ambient for buoyancy")
        return self

class PredictRequest(BaseModel):
    emission_rate: float = Field(..., gt=0, description="Q (g/s)")
    wind_speed: float = Field(..., description="u (m/s)")
    stack_height: float = Field(..., gt=0, description="h (m)")
    exit_velocity: float = Field(..., gt=0, description="ve (m/s)")
    stack_diameter: float = Field(..., gt=0, description="d (m)")
    stack_temperature: float = Field(..., gt=0, description="Ts (K)")
    ambient_temperature: float = Field(..., gt=0, description="Ta (K)")
    stability_class: str = Field(..., description="Stability class (A-F)")
    x: float = Field(..., gt=0, description="Downwind distance (m)")
    y: float = Field(..., description="Crosswind distance (m)")
    z: float = Field(..., ge=0, description="Height (m)")

    @field_validator("wind_speed")
    @classmethod
    def validate_wind_speed(cls, v: float) -> float:
        if v < 0.5:
            raise ValueError("Wind speed too low for valid dispersion modelling (min 0.5 m/s)")
        return v

    @field_validator("stability_class")
    @classmethod
    def validate_stability_class(cls, v: str) -> str:
        v = v.upper()
        if v not in STABILITY_CLASSES:
            raise ValueError(f"Invalid stability class. Must be one of: {', '.join(sorted(STABILITY_CLASSES))}")
        return v

    @model_validator(mode="after")
    def validate_temperatures(self) -> "PredictRequest":
        if self.stack_temperature <= self.ambient_temperature:
            raise ValueError("Stack temperature must exceed ambient for buoyancy")
        return self

class GridSimulateRequest(BaseModel):
    emission_rate: float = Field(..., gt=0)
    wind_speed: float = Field(..., ge=0.5)
    stack_height: float = Field(..., gt=0)
    exit_velocity: float = Field(..., gt=0)
    stack_diameter: float = Field(..., gt=0)
    stack_temperature: float = Field(..., gt=0)
    ambient_temperature: float = Field(..., gt=0)
    stability_class: str
    
    x_min: float = Field(100.0, gt=0)
    x_max: float = Field(5000.0, gt=0)
    x_steps: int = Field(50, gt=0, le=200)
    
    y_min: float = Field(-500.0)
    y_max: float = Field(500.0)
    y_steps: int = Field(50, gt=0, le=200)
    
    z: float = Field(0.0, ge=0)

    @model_validator(mode="after")
    def validate_grid_ranges(self) -> "GridSimulateRequest":
        if self.x_max <= self.x_min:
            raise ValueError("x_max must be greater than x_min")
        if self.y_max <= self.y_min:
            raise ValueError("y_max must be greater than y_min")
        return self

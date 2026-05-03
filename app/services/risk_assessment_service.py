"""
Risk Assessment Service

Orchestrates the complete risk assessment pipeline:
1. Physics calculations (plume rise, dispersion)
2. Impact distance simulation
3. Risk decision logic
4. Explanation and recommendation generation (AI-powered or fallback)
5. Confidence score calculation
6. Warning generation
7. Advanced metrics (impact width, time to impact, uncertainty range)
"""

import os
import uuid
from datetime import datetime
from app.models.request import RiskAssessmentRequest
from app.models.response import RiskAssessmentResponse
from app.physics.plume_rise import (
    compute_buoyancy_flux, 
    compute_plume_rise, 
    compute_effective_height
)
from app.physics.impact_distance import compute_impact_distance
from app.physics.concentration import compute_concentration
from app.decision.risk_engine import determine_risk_level
from app.utils.confidence import calculate_confidence
from app.utils.warnings import generate_warnings
from app.utils.advanced_metrics import (
    calculate_impact_width,
    calculate_time_to_impact,
    calculate_uncertainty_range,
    assess_population_risk
)
from app.utils.health_zones import calculate_health_zones
from app.utils.gemma_explainer import generate_explanation_with_gemma


def process_risk_assessment(request: RiskAssessmentRequest, use_ai: bool = None) -> RiskAssessmentResponse:
    """
    Complete risk assessment pipeline with advanced metrics.
    
    This is the core product logic that transforms physics into decisions.
    
    Args:
        request: Risk assessment request with emission and atmospheric parameters
        use_ai: Whether to use AI for explanations (None = auto-detect from env)
    
    Returns:
        RiskAssessmentResponse: Actionable risk assessment with recommendations
    """
    # Auto-detect AI usage if not specified
    if use_ai is None:
        use_ai = os.getenv("USE_AI_EXPLANATIONS", "false").lower() == "true"
    
    # Step 1: Plume Rise Calculations
    fb = compute_buoyancy_flux(
        request.exit_velocity,
        request.stack_diameter,
        request.stack_temperature,
        request.ambient_temperature
    )
    delta_h = compute_plume_rise(fb, request.wind_speed)
    h_eff = compute_effective_height(request.stack_height, delta_h)
    
    # Step 2: Impact Distance, Peak Concentration, and Peak Distance
    impact_distance, peak_concentration, peak_distance = compute_impact_distance(
        q=request.emission_rate,
        u=request.wind_speed,
        h_eff=h_eff,
        stability_class=request.stability_class
    )
    
    # Step 3: Risk Decision
    risk_level = determine_risk_level(peak_concentration, impact_distance)
    
    # Step 4: Calculate Confidence Score
    confidence = calculate_confidence(
        wind_speed=request.wind_speed,
        stability_class=request.stability_class,
        concentration=peak_concentration
    )
    
    # Step 5: Generate Warnings
    warnings = generate_warnings(
        wind_speed=request.wind_speed,
        stability_class=request.stability_class,
        concentration=peak_concentration,
        impact_distance=impact_distance,
        stack_height=request.stack_height,
        effective_height=h_eff
    )

    # Step 6: Generate Explanation and Recommendation (Gemma-powered or fallback)
    ai_result = generate_explanation_with_gemma(
        risk_level=risk_level,
        wind_speed=request.wind_speed,
        stability_class=request.stability_class,
        impact_distance=impact_distance,
        peak_concentration=peak_concentration,
        warnings=warnings,
        use_ai=use_ai
    )
    explanation = ai_result["explanation"]
    recommendation = ai_result["recommendation"]
    
    # Step 7: Calculate Advanced Metrics
    
    # Impact width at peak distance
    impact_width = calculate_impact_width(request.stability_class, peak_distance)
    
    # Time to impact
    time_to_impact = calculate_time_to_impact(impact_distance, request.wind_speed)
    
    # Population risk assessment
    population_risk_data = assess_population_risk(request.location_type, impact_distance)
    
    # Uncertainty range (concentration with wind speed ±20%)
    from app.physics.dispersion_coeffs import compute_sigma_y, compute_sigma_z
    
    # Get dispersion coefficients at peak distance
    if peak_distance > 0:
        sy_peak = compute_sigma_y(request.stability_class, peak_distance)
        sz_peak = compute_sigma_z(request.stability_class, peak_distance)
        
        # Compute uncertainty range
        conc_min, conc_max = calculate_uncertainty_range(
            base_concentration=peak_concentration,
            wind_speed=request.wind_speed,
            compute_concentration_func=compute_concentration,
            q=request.emission_rate,
            sy=sy_peak,
            sz=sz_peak,
            y=0.0,
            z=0.0,
            h=h_eff
        )
        
        uncertainty_range = {
            "min_concentration": conc_min,
            "max_concentration": conc_max
        }
    else:
        uncertainty_range = None
    
    return RiskAssessmentResponse(
        risk_level=risk_level,
        peak_concentration=peak_concentration,
        impact_distance_meters=impact_distance,
        effective_height=h_eff,
        explanation=explanation,
        recommendation=recommendation,
        confidence=confidence,
        warnings=warnings,
        # Advanced metrics
        impact_width_meters=impact_width if impact_width > 0 else None,
        time_to_impact_minutes=time_to_impact if time_to_impact > 0 else None,
        peak_distance_meters=peak_distance if peak_distance > 0 else None,
        population_risk=population_risk_data.get("population_risk"),
        uncertainty_range=uncertainty_range,
        assessment_id=f"RISK-{str(uuid.uuid4())[:8].upper()}",
        timestamp=datetime.now().isoformat(),
        ai_used=ai_result.get("ai_used", False),
        health_zones=calculate_health_zones(peak_concentration, impact_distance)
    )

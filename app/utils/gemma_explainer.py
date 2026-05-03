"""
Gemma Explanation Engine (OpenRouter Edition)

This module generates human-readable risk explanations and actionable 
recommendations using Gemma models via OpenRouter.

DESIGNED FOR: google/gemma-4-31b-it
"""

import os
import requests
import json
from typing import Dict, Any, Optional


def generate_explanation_with_gemma(
    risk_level: str,
    wind_speed: float,
    stability_class: str,
    impact_distance: float,
    peak_concentration: float,
    warnings: list,
    use_ai: bool = True
) -> Dict[str, Any]:
    """
    Orchestrates the generation of AI explanations or falls back to rule-based logic.
    """
    
    if not use_ai:
        return _generate_fallback(risk_level, wind_speed, stability_class, impact_distance)

    # Load configuration
    api_key = os.getenv("OPENROUTER_API_KEY")
    model_id = os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it")
    
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not found. Using fallback.")
        return _generate_fallback(risk_level, wind_speed, stability_class, impact_distance)

    # Format warnings for prompt inclusion
    warnings_text = ""
    if warnings:
        warnings_text = "\nActive warnings:\n" + "\n".join(f"- {w}" for w in warnings[:3])

    # Construct the prompt
    prompt = f"""You are an environmental risk expert analyzing an industrial emission event.

Given:
* Risk level: {risk_level}
* Wind speed: {wind_speed} m/s
* Atmospheric stability class: {stability_class}
* Impact distance: {impact_distance:.0f} meters
* Peak concentration: {peak_concentration:.2e} g/m³{warnings_text}

Explain clearly in 3-4 sentences:
1. Why this risk level occurred
2. How wind speed and stability class affected dispersion
3. What this means for people in nearby areas

Then provide a short, actionable recommendation (1-2 sentences).

Keep language simple and human-friendly.

Format your response exactly as:
EXPLANATION: [Your explanation here]
RECOMMENDATION: [Your recommendation here]"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://plu-monitor.local", # Required by OpenRouter
                "X-Title": "Plu Emission Monitor",
                "Content-Type": "application/json"
            },
            json={
                "model": model_id,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                text = result["choices"][0]["message"]["content"]
                if text:
                    return _parse_ai_response(text)
                
        # If API returns error
        print(f"OpenRouter API returned code {response.status_code}: {response.text}")
        
    except Exception as e:
        print(f"OpenRouter explanation generation failed: {e}. Falling back.")

    return _generate_fallback(risk_level, wind_speed, stability_class, impact_distance)


def _parse_ai_response(text: str) -> Dict[str, Any]:
    """Parses the raw text into explanation and recommendation."""
    explanation = ""
    recommendation = ""
    
    # Simple parsing logic
    if "RECOMMENDATION:" in text:
        parts = text.split("RECOMMENDATION:")
        explanation = parts[0].replace("EXPLANATION:", "").strip()
        recommendation = parts[1].strip()
    elif "EXPLANATION:" in text:
        explanation = text.replace("EXPLANATION:", "").strip()
        recommendation = "Follow established safety protocols for your zone."
    else:
        # If model doesn't follow format perfectly
        explanation = text.strip()
        recommendation = "Refer to the regional safety map for specific actions."

    return {
        "explanation": explanation,
        "recommendation": recommendation,
        "ai_used": True
    }


def _generate_fallback(
    risk_level: str,
    wind_speed: float,
    stability_class: str,
    impact_distance: float
) -> Dict[str, Any]:
    """Deterministic rule-based fallback logic."""
    
    # Generic physics-based explanation
    stability_map = {
        "A": "highly unstable and turbulent",
        "B": "moderately unstable",
        "C": "slightly unstable",
        "D": "neutral",
        "E": "slightly stable",
        "F": "highly stable and stagnant"
    }
    
    stab_desc = stability_map.get(stability_class, "variable")
    
    explanation = f"The {risk_level} risk level is determined by a peak concentration occurring approximately {impact_distance:.0f}m from the source. "
    explanation += f"A wind speed of {wind_speed} m/s and atmospheric stability class {stability_class} ({stab_desc}) "
    
    if wind_speed < 2:
        explanation += "resulted in poor horizontal dispersion, causing higher local accumulation. "
    else:
        explanation += "facilitated moderate dispersion through the air column. "
        
    if stability_class in ["E", "F"]:
        explanation += "The stable atmosphere prevented vertical mixing, trapping the plume near the ground."
    else:
        explanation += "The unstable atmosphere allowed for vertical plume rise, potentially reducing ground-level impacts."

    recommendations = {
        "LOW": "Continue routine monitoring. No immediate public health action required.",
        "MEDIUM": "Increase sensor frequency. Advise vulnerable populations to limit outdoor exposure in downwind zones.",
        "HIGH": "Implement immediate emission reduction protocols. Issue local health advisory for areas within impact radius."
    }

    return {
        "explanation": explanation,
        "recommendation": recommendations.get(risk_level, "Follow standard operating procedures."),
        "ai_used": False
    }

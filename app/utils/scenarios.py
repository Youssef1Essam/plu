"""
Scenario Presets

Predefined realistic emission scenarios for common industrial sources.
"""

from typing import Dict, Any

# Predefined realistic scenarios
SCENARIOS = {
    "power_plant": {
        "name": "Coal-Fired Power Plant",
        "description": "Large coal-fired power plant with tall stack and high exit velocity",
        "emission_rate": 100.0,
        "wind_speed": 5.0,
        "stack_height": 150.0,
        "exit_velocity": 25.0,
        "stack_diameter": 4.0,
        "stack_temperature": 450.0,
        "ambient_temperature": 293.0,
        "stability_class": "D"
    },
    "factory": {
        "name": "Industrial Factory",
        "description": "Medium-sized industrial facility with moderate emissions",
        "emission_rate": 30.0,
        "wind_speed": 4.0,
        "stack_height": 50.0,
        "exit_velocity": 12.0,
        "stack_diameter": 2.0,
        "stack_temperature": 380.0,
        "ambient_temperature": 293.0,
        "stability_class": "D"
    },
    "waste_burning": {
        "name": "Waste Incinerator",
        "description": "Waste burning facility with lower stack and variable emissions",
        "emission_rate": 20.0,
        "wind_speed": 3.0,
        "stack_height": 30.0,
        "exit_velocity": 8.0,
        "stack_diameter": 1.5,
        "stack_temperature": 350.0,
        "ambient_temperature": 293.0,
        "stability_class": "D"
    }
}


def get_scenario(scenario_name: str) -> Dict[str, Any]:
    """
    Get predefined scenario parameters.
    
    Args:
        scenario_name: Name of the scenario (power_plant, factory, waste_burning)
    
    Returns:
        Dict with scenario parameters
    
    Raises:
        ValueError: If scenario name is invalid
    """
    scenario = SCENARIOS.get(scenario_name.lower())
    if scenario is None:
        valid_scenarios = ", ".join(SCENARIOS.keys())
        raise ValueError(f"Invalid scenario. Must be one of: {valid_scenarios}")
    return scenario.copy()


def list_scenarios() -> Dict[str, Dict[str, Any]]:
    """
    List all available scenarios.
    
    Returns:
        Dict mapping scenario names to their parameters
    """
    return SCENARIOS.copy()

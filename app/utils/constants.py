# Physical constants
GRAVITY = 9.81  # m/s^2

# Stability Class Mappings for Alpha (σy)
ALPHA_MAP = {
    "A": 0.22,
    "B": 0.16,
    "C": 0.11,
    "D": 0.08,
    "E": 0.06,
    "F": 0.04
}

# Risk Thresholds (g/m^3)
# LOW: C < 0.0001
# MEDIUM: 0.0001 <= C < 0.001
# HIGH: C >= 0.001
THRESHOLD_LOW = 0.0001
THRESHOLD_MEDIUM = 0.001

STABILITY_CLASSES = set(ALPHA_MAP.keys())

# Impact Distance Simulation Parameters
IMPACT_DISTANCE_MAX = 5000  # meters
IMPACT_DISTANCE_STEP = 50   # meters

# Decision Thresholds for Impact Distance
DISTANCE_SHORT = 800    # meters
DISTANCE_MEDIUM = 2000  # meters

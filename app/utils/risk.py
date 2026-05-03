from app.utils.constants import THRESHOLD_LOW, THRESHOLD_MEDIUM

def classify_risk(concentration: float) -> str:
    """
    Classify risk level based on pollutant concentration.
    """
    if concentration < THRESHOLD_LOW:
        return "low"
    elif concentration < THRESHOLD_MEDIUM:
        return "medium"
    else:
        return "high"

def build_notes(stability_class: str, effective_height: float, x: float) -> str:
    """
    Generate contextual notes for the prediction.
    """
    notes = [f"Stability class {stability_class} used for dispersion coefficients."]
    
    if effective_height > 200:
        notes.append("High plume rise detected; concentration may be lower at ground level near the source.")
    
    if x < 100:
        notes.append("Receptor is very close to the source; results may have higher uncertainty.")
        
    return " ".join(notes)

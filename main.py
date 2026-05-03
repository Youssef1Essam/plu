from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routers import risk_assessment, impact_simulation, scenarios, predict, simulate, egypt

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Plu - Emission Risk Intelligence",
    description="Built for Cairo. Works anywhere. Scientific decision system for industrial emission risk assessment.",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174",
        "http://localhost:4173"
    ],  # Vite dev and preview
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Primary product endpoints
app.include_router(risk_assessment.router, tags=["Risk Assessment"])
app.include_router(impact_simulation.router, tags=["Impact Analysis"])

# Scenario-based endpoints (NEW)
app.include_router(scenarios.router, tags=["Scenarios"])

# Egypt-specific endpoints (NEW)
app.include_router(egypt.router, tags=["Egypt Analysis"])

# Legacy endpoints (for backward compatibility)
app.include_router(predict.router, tags=["Legacy - Prediction"])
app.include_router(simulate.router, tags=["Legacy - Simulation"])

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Industrial Emission Risk Monitor",
        "version": "2.2.0",
        "description": "Decision system for emission risk assessment",
        "features": {
            "v2.2.0": [
                "Impact width calculation",
                "Time to impact estimation",
                "Peak location tracking",
                "Population risk hints",
                "Uncertainty range analysis",
                "AI-powered explanations (Gemma 4 via Ollama or HuggingFace)"
            ],
            "v2.1.0": [
                "Scenario presets",
                "Scenario-based prediction",
                "Auto weather mode",
                "Confidence scores",
                "Warning generation"
            ]
        },
        "ai_enabled": os.getenv("USE_AI_EXPLANATIONS", "false").lower() == "true"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

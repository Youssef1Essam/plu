from fastapi import APIRouter, HTTPException
from app.models.request import PredictRequest
from app.models.response import PredictResponse
from app.services.dispersion_service import process_prediction

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict_concentration(request: PredictRequest):
    """
    Predict pollutant concentration at a specific receptor point (x, y, z).
    """
    try:
        return process_prediction(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal computation error: {str(e)}")

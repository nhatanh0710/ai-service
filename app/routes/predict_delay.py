from fastapi import APIRouter

from app.schemas.predict import (
    PredictDelayRequest,
    PredictDelayResponse,
)

from app.services.prediction_service import (
    PredictionService,
)

router = APIRouter(
    prefix="/predict-delay",
    tags=["Predict Delay"],
)


@router.post(
    "",
    response_model=PredictDelayResponse,
)
def predict_delay(
    request: PredictDelayRequest,
):

    """
    Predict task delay risk.
    """

    return PredictionService.predict(request)
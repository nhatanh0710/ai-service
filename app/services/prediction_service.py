import numpy as np

from app.schemas.predict import (
    PredictDelayRequest,
    PredictDelayResponse,
)

from app.utils.model_loader import (
    get_model,
    get_encoders,
)


class PredictionService:
    """
    AI Prediction Service
    Predict Task Delay Risk using Random Forest.
    """

    @staticmethod
    def predict(request: PredictDelayRequest) -> PredictDelayResponse:

        # ==========================================================
        # Load trained model & encoders
        # ==========================================================

        model = get_model()
        encoders = get_encoders()

        # ==========================================================
        # Prepare feature vector
        # Feature order MUST match training dataset.
        # ==========================================================

        features = np.array(
            [[
                request.priority,
                request.estimate_time,
                request.actual_time,
                request.remaining_days,
                request.current_progress,
                request.assignee_count,
                request.average_workload,
                request.task_complexity,
            ]]
        )

        # ==========================================================
        # Predict class
        # ==========================================================

        prediction = model.predict(features)[0]

        # ==========================================================
        # Predict probability
        # Example:
        # LOW    = 0.10
        # MEDIUM = 0.18
        # HIGH   = 0.72
        # ==========================================================

        probabilities = model.predict_proba(features)[0]

        # Decode prediction
        risk_encoder = encoders["risk_encoder"]

        risk = risk_encoder.inverse_transform(
            [prediction]
        )[0]

        # ==========================================================
        # Confidence
        # Highest probability among all classes.
        # ==========================================================

        confidence = round(
            float(np.max(probabilities) * 100),
            2,
        )

        # ==========================================================
        # Risk Score
        #
        # Risk Score represents the probability of HIGH risk.
        # This value is more meaningful for visualization
        # than simply converting LOW/MEDIUM/HIGH manually.
        # ==========================================================

        high_index = list(
            risk_encoder.classes_
        ).index("HIGH")

        risk_score = round(
            float(probabilities[high_index] * 100),
            2,
        )

        # ==========================================================
        # Summary
        # ==========================================================

        summary = PredictionService.generate_summary(
            risk=risk,
            progress=request.current_progress,
            remaining_days=request.remaining_days,
        )

        # ==========================================================
        # Return response
        # ==========================================================

        return PredictDelayResponse(
            current_progress=request.current_progress,
            remaining_days=request.remaining_days,
            risk_score=risk_score,
            risk=risk,
            confidence=confidence,
            summary=summary,
        )

    @staticmethod
    def generate_summary(
        risk: str,
        progress: float,
        remaining_days: int,
    ) -> str:
        """
        Generate human-readable prediction summary.
        """

        if risk == "HIGH":
            return (
                f"Task has a HIGH delay risk. "
                f"Current progress is {progress:.0f}% "
                f"with only {remaining_days} remaining day(s)."
            )

        if risk == "MEDIUM":
            return (
                f"Task has a MEDIUM delay risk. "
                f"Current progress is {progress:.0f}%. "
                "Project manager should monitor this task closely."
            )

        return (
            f"Task has a LOW delay risk. "
            "Current progress is on track with the planned schedule."
        )
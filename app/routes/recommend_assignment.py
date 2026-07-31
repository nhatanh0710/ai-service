import joblib
import pandas as pd

from fastapi import APIRouter

from app.schemas.recommend_assignment import (
    RecommendAssignmentRequest,
    RecommendAssignmentResponse,
    Recommendation,
)

router = APIRouter()

# ============================================================
# Load model một lần khi server khởi động
# ============================================================

model = joblib.load(
    "saved_models/assignment_model.pkl"
)


@router.post(
    "/recommend-assignment",
    response_model=RecommendAssignmentResponse,
)
def recommend_assignment(
    request: RecommendAssignmentRequest,
):

    members = []

    for member in request.members:

        members.append(
            {
                "user_id": member.user_id,
                "skill_match": member.skill_match,
                "experience_level": member.experience_level,
                "current_tasks": member.current_tasks,
                "max_tasks": member.max_tasks,
                "performance_score": member.performance_score,
                "completed_tasks": member.completed_tasks,
                "working_hours_per_day": member.working_hours_per_day,
            }
        )

    df = pd.DataFrame(members)

    X = df[
        [
            "skill_match",
            "experience_level",
            "current_tasks",
            "max_tasks",
            "performance_score",
            "completed_tasks",
            "working_hours_per_day",
        ]
    ]

    probabilities = model.predict_proba(X)

    recommendations = []

    for index, probability in enumerate(probabilities):

        recommendations.append(
            Recommendation(
                user_id=df.iloc[index]["user_id"],
                score=round(float(probability[1]) * 100, 2),
            )
        )

    recommendations.sort(
        key=lambda x: x.score,
        reverse=True,
    )

    return RecommendAssignmentResponse(
        recommendations=recommendations[:3]
    )
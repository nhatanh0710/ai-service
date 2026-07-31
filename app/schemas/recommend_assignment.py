from pydantic import BaseModel


class MemberFeatures(BaseModel):
    user_id: str

    skill_match: float
    experience_level: int

    current_tasks: int
    max_tasks: int

    performance_score: float
    completed_tasks: int

    working_hours_per_day: int


class RecommendAssignmentRequest(BaseModel):
    members: list[MemberFeatures]


from pydantic import BaseModel


class Recommendation(BaseModel):
    user_id: str
    score: float


class RecommendAssignmentResponse(BaseModel):
    recommendations: list[Recommendation]
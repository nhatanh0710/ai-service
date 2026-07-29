from pydantic import BaseModel, Field


class PredictDelayRequest(BaseModel):
    """
    Request schema for Task Delay Risk Prediction
    """

    priority: int = Field(
        ...,
        ge=0,
        le=3,
        description="Task priority (0=LOW, 1=MEDIUM, 2=HIGH, 3=URGENT)",
    )

    estimate_time: float = Field(
        ...,
        gt=0,
        description="Estimated working hours",
    )

    actual_time: float = Field(
        ...,
        ge=0,
        description="Actual logged working hours",
    )

    remaining_days: int = Field(
        ...,
        ge=0,
        description="Remaining days until deadline",
    )

    current_progress: float = Field(
        ...,
        ge=0,
        le=100,
        description="Current task progress (%)",
    )

    assignee_count: int = Field(
        ...,
        ge=0,
        description="Number of task assignees",
    )

    average_workload: float = Field(
        ...,
        ge=0,
        description="Average workload of assignees (hours/day)",
    )

    task_complexity: int = Field(
        ...,
        ge=0,
        le=3,
        description="Task complexity (0=EASY, 1=MEDIUM, 2=HARD, 3=VERY_HARD)",
    )


class PredictDelayResponse(BaseModel):
    """
    Response schema for Task Delay Risk Prediction
    """

    current_progress: float

    remaining_days: int

    risk_score: float

    risk: str

    confidence: float

    summary: str
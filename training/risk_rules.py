import random

from feature_config import (
    Priority,
    TaskComplexity,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    NOISE_RATE,
)


def calculate_risk_score(
    priority: Priority,
    estimate_time: int,
    actual_time: float,
    remaining_days: int,
    current_progress: int,
    assignee_count: int,
    average_workload: float,
    task_complexity: TaskComplexity,
) -> int:
    """
    Tính điểm rủi ro (0 - 100).

    Các trọng số được xây dựng dựa trên nghiệp vụ quản lý dự án:
    - Current Progress
    - Remaining Days
    - Actual Time / Estimate Time
    - Workload
    - Priority
    - Task Complexity

    Sau đó áp dụng thêm một số Business Rules để mô phỏng dữ liệu thực tế.
    """

    score = 0

    # ==========================================================
    # Current Progress
    # Tiến độ càng thấp thì rủi ro càng cao
    # ==========================================================

    if current_progress < 20:
        score += 35
    elif current_progress < 40:
        score += 25
    elif current_progress < 60:
        score += 15
    elif current_progress < 80:
        score += 5

    # ==========================================================
    # Remaining Days
    # Deadline càng gần thì nguy cơ càng cao
    # ==========================================================

    if remaining_days <= 1:
        score += 30
    elif remaining_days <= 3:
        score += 18
    elif remaining_days <= 7:
        score += 8

    # ==========================================================
    # Actual Time / Estimate Time
    # Nếu thời gian thực tế đã vượt estimate thì tăng rủi ro
    # ==========================================================

    time_ratio = actual_time / estimate_time

    if time_ratio >= 1.2:
        score += 15
    elif time_ratio >= 1.0:
        score += 8

    # ==========================================================
    # Average Workload
    # Thành viên càng bận thì khả năng trễ càng cao
    # ==========================================================

    if average_workload >= 10:
        score += 18
    elif average_workload >= 8:
        score += 10
    elif average_workload >= 6:
        score += 5

    # ==========================================================
    # Priority
    # ==========================================================

    if priority == Priority.URGENT:
        score += 12
    elif priority == Priority.HIGH:
        score += 8
    elif priority == Priority.MEDIUM:
        score += 4

    # ==========================================================
    # Task Complexity
    # ==========================================================

    if task_complexity == TaskComplexity.VERY_HARD:
        score += 10
    elif task_complexity == TaskComplexity.HARD:
        score += 7
    elif task_complexity == TaskComplexity.MEDIUM:
        score += 3

    # ==========================================================
    # Business Rules
    # ==========================================================

    # Deadline rất gần nhưng tiến độ rất thấp
    if remaining_days <= 2 and current_progress < 40:
        score += 12

    # Đã vượt estimate nhưng tiến độ vẫn thấp
    if actual_time > estimate_time and current_progress < 70:
        score += 10

    # Task rất khó nhưng chỉ có 1 người làm
    if (
        task_complexity == TaskComplexity.VERY_HARD
        and assignee_count == 1
    ):
        score += 8

    # Workload rất cao và tiến độ thấp
    if average_workload >= 10 and current_progress < 50:
        score += 8

    # Tiến độ rất tốt và còn nhiều thời gian
    if current_progress >= 90 and remaining_days >= 5:
        score -= 12

    # Tiến độ tốt và workload thấp
    if current_progress >= 80 and average_workload <= 5:
        score -= 8

    # Giới hạn điểm từ 0 - 100
    score = max(0, min(score, 100))

    return score


def classify_risk(score: int) -> str:
    """
    Chuyển đổi Risk Score thành mức độ rủi ro.
    """

    if score >= 70:
        return RISK_HIGH

    if score >= 40:
        return RISK_MEDIUM

    return RISK_LOW


def apply_noise(risk: str) -> str:
    """
    Thêm một lượng nhỏ nhiễu để dataset
    gần với dữ liệu thực tế hơn.
    """

    if random.random() >= NOISE_RATE:
        return risk

    if risk == RISK_HIGH:
        return random.choice(
            [
                RISK_HIGH,
                RISK_MEDIUM,
            ]
        )

    if risk == RISK_MEDIUM:
        return random.choice(
            [
                RISK_LOW,
                RISK_MEDIUM,
                RISK_HIGH,
            ]
        )

    return random.choice(
        [
            RISK_LOW,
            RISK_MEDIUM,
        ]
    )
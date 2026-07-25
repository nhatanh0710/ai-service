import random

from feature_config import (
    Priority,
    TaskComplexity,
)


# ==========================================================
# Priority
# ==========================================================

def generate_priority():

    return random.choices(
        population=[
            Priority.LOW,
            Priority.MEDIUM,
            Priority.HIGH,
            Priority.URGENT,
        ],
        weights=[
            20,
            40,
            30,
            10,
        ],
        k=1,
    )[0]


# ==========================================================
# Estimate Time
# ==========================================================

def generate_estimate_time(priority: Priority):

    if priority == Priority.LOW:
        return random.randint(2, 8)

    if priority == Priority.MEDIUM:
        return random.randint(4, 16)

    if priority == Priority.HIGH:
        return random.randint(8, 24)

    return random.randint(16, 40)


# ==========================================================
# Task Complexity
# ==========================================================

def generate_task_complexity(estimate_time: int):

    if estimate_time <= 4:
        return TaskComplexity.EASY

    if estimate_time <= 12:
        return TaskComplexity.MEDIUM

    if estimate_time <= 24:
        return TaskComplexity.HARD

    return TaskComplexity.VERY_HARD


# ==========================================================
# Assignee Count
# ==========================================================

def generate_assignee_count(complexity: TaskComplexity):

    if complexity == TaskComplexity.EASY:
        return 1

    if complexity == TaskComplexity.MEDIUM:
        return random.randint(1, 2)

    if complexity == TaskComplexity.HARD:
        return random.randint(2, 3)

    return random.randint(3, 5)


# ==========================================================
# Average Workload
# ==========================================================

def generate_average_workload(assignee_count: int):

    if assignee_count == 1:
        return round(random.uniform(7, 12), 1)

    if assignee_count == 2:
        return round(random.uniform(5, 10), 1)

    if assignee_count == 3:
        return round(random.uniform(4, 8), 1)

    return round(random.uniform(2, 6), 1)


# ==========================================================
# Remaining Days
# ==========================================================

def generate_remaining_days(estimate_time: int):

    if estimate_time <= 4:
        return random.randint(1, 3)

    if estimate_time <= 12:
        return random.randint(2, 7)

    if estimate_time <= 24:
        return random.randint(4, 10)

    return random.randint(6, 15)


# ==========================================================
# Current Progress
# ==========================================================

def generate_current_progress(
    remaining_days: int,
    average_workload: float,
) -> int:
    """
    Mô phỏng current_progress được tính từ checklist_progress.
    checklist_progress không lưu vào dataset, chỉ dùng nội bộ.
    """

    # Sinh checklist progress theo thời gian còn lại

    if remaining_days <= 2:
        checklist_progress = random.randint(70, 100)

    elif remaining_days <= 5:
        checklist_progress = random.randint(45, 90)

    elif remaining_days <= 10:
        checklist_progress = random.randint(20, 75)

    else:
        checklist_progress = random.randint(0, 55)

    # Workload càng cao thì checklist hoàn thành chậm hơn

    if average_workload >= 10:
        checklist_progress -= random.randint(12, 20)

    elif average_workload >= 8:
        checklist_progress -= random.randint(6, 12)

    checklist_progress = max(
        0,
        min(100, checklist_progress),
    )

    # Task Progress được tính từ Checklist Progress
    # Thêm một ít nhiễu để mô phỏng dữ liệu thực

    noise = random.randint(-3, 3)

    current_progress = checklist_progress + noise

    current_progress = max(
        0,
        min(100, current_progress),
    )

    return current_progress

# ==========================================================
# Actual Time
# ==========================================================

def generate_actual_time(
    estimate_time: int,
    current_progress: int,
):

    ratio = current_progress / 100

    actual = estimate_time * ratio

    noise = random.uniform(-1.5, 1.5)

    actual += noise

    actual = max(0.5, actual)

    return round(actual, 1)
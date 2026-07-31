import math
import random

import pandas as pd

NUM_RECORDS = 10000

# ============================================================
# Encode Experience Level
# RandomForest chỉ làm việc với dữ liệu số.
# ============================================================

EXPERIENCE_LEVELS = {
    "fresher": 0,
    "junior": 1,
    "middle": 2,
    "senior": 3,
}


# ============================================================
# Sigmoid
#
# Chỉ dùng để sinh LABEL cho dataset.
# KHÔNG phải thuật toán AI của hệ thống.
#
# AI thực tế vẫn là RandomForestClassifier.
# ============================================================

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# ============================================================
# Sinh hồ sơ Project Member
#
# Các thuộc tính có liên quan với nhau.
#
# Ví dụ:
# Senior
#     -> performance cao
#     -> completed nhiều
#     -> max task cao
# ============================================================

def generate_member():

    level = random.choices(
        population=["fresher", "junior", "middle", "senior"],
        weights=[20, 35, 30, 15],
        k=1,
    )[0]

    if level == "fresher":

        performance = random.randint(40, 65)
        completed = random.randint(0, 8)
        max_tasks = random.randint(2, 3)

    elif level == "junior":

        performance = random.randint(60, 80)
        completed = random.randint(8, 25)
        max_tasks = random.randint(3, 5)

    elif level == "middle":

        performance = random.randint(75, 92)
        completed = random.randint(20, 50)
        max_tasks = random.randint(4, 6)

    else:

        performance = random.randint(88, 100)
        completed = random.randint(40, 80)
        max_tasks = random.randint(5, 8)

    current_tasks = random.randint(0, max_tasks)

    working_hours = random.choice([4, 6, 8])

    return {
        "experience_level": EXPERIENCE_LEVELS[level],
        "performance_score": performance,
        "completed_tasks": completed,
        "max_tasks": max_tasks,
        "current_tasks": current_tasks,
        "working_hours_per_day": working_hours,
    }


rows = []

for _ in range(NUM_RECORDS):

    member = generate_member()

    # ========================================================
    # Skill Match
    #
    # Thực tế Backend sẽ tính:
    #
    # skill_match =
    # số tag trùng giữa
    # Task.tags
    # và
    # ProjectMember.skills
    #
    # Dataset chỉ mô phỏng kết quả.
    #
    # 0.00 = không trùng
    # 0.33 = trùng ít
    # 0.67 = trùng khá nhiều
    # 1.00 = trùng hoàn toàn
    # ========================================================

    skill_match = random.choices(
        population=[0.0, 0.33, 0.67, 1.0],
        weights=[20, 30, 30, 20],
        k=1,
    )[0]

    # ========================================================
    # Assignment Score
    #
    # KHÔNG phải Rule-based.
    #
    # Chỉ dùng để sinh LABEL cho dataset.
    #
    # RandomForest sẽ học từ dataset này.
    #
    # Ý nghĩa:
    #
    # + Skill Match cao
    # + Performance cao
    # + Kinh nghiệm nhiều
    #
    # => khả năng được giao việc cao hơn.
    #
    # Ngược lại:
    #
    # + Đang quá nhiều task
    #
    # => giảm khả năng được giao.
    # ========================================================

    score = 0

    # Chuyên môn phù hợp
    score += skill_match * 45

    # Hiệu suất làm việc
    score += member["performance_score"] * 0.35

    # Kinh nghiệm
    score += member["completed_tasks"] * 0.20

    # Level
    score += member["experience_level"] * 8

    # Đang có nhiều việc
    score -= member["current_tasks"] * 8

    # Đã đạt ngưỡng tối đa task
    if member["current_tasks"] >= member["max_tasks"]:
        score -= 15

    # ========================================================
    # Sinh Label
    # ========================================================

    probability = sigmoid((score - 40) / 10)

    assigned = 1 if random.random() < probability else 0

    rows.append(
        {
            "skill_match": skill_match,
            "experience_level": member["experience_level"],
            "current_tasks": member["current_tasks"],
            "max_tasks": member["max_tasks"],
            "performance_score": member["performance_score"],
            "completed_tasks": member["completed_tasks"],
            "working_hours_per_day": member["working_hours_per_day"],
            "assigned": assigned,
        }
    )

# ============================================================
# Export Dataset
# ============================================================

df = pd.DataFrame(rows)

df.to_csv(
    "datasets/assignment_dataset.csv",
    index=False,
)

print("=" * 60)
print("Assignment Dataset Generated Successfully")
print("=" * 60)

print(f"Total Records : {len(df)}")
print()

print(df["assigned"].value_counts())
print()

print(df.describe())

print("=" * 60)
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv("datasets/assignment_dataset.csv")

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

y = df["assigned"]

# ============================================================
# Load Model
# ============================================================

model = joblib.load(
    "saved_models/assignment_model.pkl"
)

# ============================================================
# Prediction
# ============================================================

predictions = model.predict(X)

# ============================================================
# Accuracy
# ============================================================

accuracy = accuracy_score(
    y,
    predictions,
)

print("=" * 60)
print("Assignment Recommendation Model Evaluation")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")

# ============================================================
# Classification Report
# ============================================================

print()
print("=" * 60)
print("Classification Report")
print("=" * 60)

print(
    classification_report(
        y,
        predictions,
    )
)

# ============================================================
# Confusion Matrix
# ============================================================

print("=" * 60)
print("Confusion Matrix")
print("=" * 60)

print(
    confusion_matrix(
        y,
        predictions,
    )
)

# ============================================================
# Feature Importance
# ============================================================

print()
print("=" * 60)
print("Feature Importance")
print("=" * 60)

features = [
    "skill_match",
    "experience_level",
    "current_tasks",
    "max_tasks",
    "performance_score",
    "completed_tasks",
    "working_hours_per_day",
]

importance = model.feature_importances_

importance_df = (
    pd.DataFrame(
        {
            "Feature": features,
            "Importance": importance,
        }
    )
    .sort_values(
        by="Importance",
        ascending=False,
    )
)

print(importance_df)

print("=" * 60)
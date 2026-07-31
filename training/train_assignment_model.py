import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv("datasets/assignment_dataset.csv")

# ============================================================
# Feature / Label
# ============================================================

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
# Train / Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print("=" * 60)
print("Dataset Information")
print("=" * 60)

print(f"Total Records : {len(df)}")
print(f"Train Records : {len(X_train)}")
print(f"Test Records  : {len(X_test)}")

# ============================================================
# Random Forest
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
)

model.fit(X_train, y_train)

# ============================================================
# Evaluate
# ============================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print()
print("=" * 60)
print(f"Accuracy : {accuracy:.4f}")
print("=" * 60)

# ============================================================
# Save Model
# ============================================================

joblib.dump(
    model,
    "saved_models/assignment_model.pkl",
)

print()
print("Assignment Model Saved Successfully.")
"""
evaluate_model.py

Mục đích:
- Đánh giá chất lượng mô hình Machine Learning.
- Hiển thị Accuracy, Precision, Recall, F1-score.
- Hiển thị Confusion Matrix.
"""

import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from sklearn.model_selection import train_test_split

from label_encoder import DatasetEncoder


# ==========================================================
# Paths
# ==========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    CURRENT_DIR,
    "..",
    "datasets",
    "task_delay_dataset.csv",
)

MODEL_PATH = os.path.join(
    CURRENT_DIR,
    "..",
    "saved_models",
    "task_delay_model.pkl",
)


def main():

    print("=" * 60)
    print("LOAD DATASET")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)

    encoder = DatasetEncoder()

    df = encoder.fit_transform(df)

    print()

    print("=" * 60)
    print("LABEL MAPPING")
    print("=" * 60)

    for index, label in enumerate(
        encoder.risk_encoder.classes_
    ):
        print(f"{index} -> {label}")

    X = df.drop(columns=["risk"])

    y = df["risk"]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = joblib.load(MODEL_PATH)

    predictions = model.predict(X_test)

    print()

    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    print(f"Accuracy : {accuracy:.4f}")

    print()

    print("=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)

    print(
        classification_report(
            y_test,
            predictions,
        )
    )

    print()

    print("=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    print()

    print("=" * 60)
    print("FEATURE IMPORTANCE")
    print("=" * 60)

    feature_importance = pd.DataFrame(
        {
            "Feature": X.columns,
            "Importance": model.feature_importances_,
        }
    )

    feature_importance = feature_importance.sort_values(
        by="Importance",
        ascending=False,
    )

    print(feature_importance.to_string(index=False))


if __name__ == "__main__":
    main()
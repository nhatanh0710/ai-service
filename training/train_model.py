"""
train_model.py

Mục đích:
- Đọc dataset
- Encode dữ liệu
- Chia tập Train/Test
- Huấn luyện Random Forest
- Đánh giá sơ bộ Accuracy
- Lưu Model
- Lưu Label Encoder
"""

import os

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

ENCODER_PATH = os.path.join(
    CURRENT_DIR,
    "..",
    "saved_models",
    "label_encoders.pkl",
)


def main():

    print("=" * 60)
    print("LOAD DATASET")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)

    print(df.head())

    # ======================================================
    # Encode categorical columns
    # ======================================================

    encoder = DatasetEncoder()

    df = encoder.fit_transform(df)

    # ======================================================
    # Feature & Label
    # ======================================================

    X = df.drop(columns=["risk"])

    y = df["risk"]

    # ======================================================
    # Train / Test Split
    # ======================================================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print()

    print("=" * 60)
    print("TRAIN / TEST SPLIT")
    print("=" * 60)

    print(f"Train: {len(X_train)}")

    print(f"Test : {len(X_test)}")

    # ======================================================
    # Random Forest
    # ======================================================

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(
        X_train,
        y_train,
    )

    # ======================================================
    # Prediction
    # ======================================================

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    print()

    print("=" * 60)
    print("MODEL RESULT")
    print("=" * 60)

    print(f"Accuracy : {accuracy:.4f}")

    # ======================================================
    # Save model
    # ======================================================

    joblib.dump(
        model,
        MODEL_PATH,
    )

    encoder.save(
        ENCODER_PATH,
    )

    print()

    print("=" * 60)
    print("MODEL SAVED")
    print("=" * 60)

    print(MODEL_PATH)

    print(ENCODER_PATH)


if __name__ == "__main__":
    main()
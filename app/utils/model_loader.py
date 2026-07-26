from pathlib import Path

import joblib


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "saved_models" / "task_delay_model.pkl"
ENCODER_PATH = BASE_DIR / "saved_models" / "label_encoders.pkl"


# ==========================================================
# Global Objects
# ==========================================================

model = None
encoders = None


# ==========================================================
# Load Model
# ==========================================================

def load_model():
    """
    Load AI model and label encoders into memory.

    This function should only be executed once
    when the FastAPI application starts.
    """

    global model
    global encoders

    if model is None:
        model = joblib.load(MODEL_PATH)

    if encoders is None:
        encoders = joblib.load(ENCODER_PATH)

    print("==================================================")
    print("AI Model Loaded Successfully")
    print("==================================================")


# ==========================================================
# Getter Functions
# ==========================================================

def get_model():
    return model


def get_encoders():
    return encoders
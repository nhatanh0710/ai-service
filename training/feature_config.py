
from pathlib import Path
from enum import IntEnum

# ==========================
# Priority
# ==========================

class Priority(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3


# ==========================
# Task Complexity
# ==========================

class TaskComplexity(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    VERY_HARD = 3


# ==========================
# Dataset Configuration
# ==========================


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_SIZE = 10_000

OUTPUT_PATH = BASE_DIR / "datasets" / "task_delay_dataset.csv"

# ==========================
# Label
# ==========================

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"


# ==========================
# Dataset Distribution
# ==========================

TARGET_DISTRIBUTION = {
    RISK_LOW: 0.50,
    RISK_MEDIUM: 0.35,
    RISK_HIGH: 0.15,
}


# ==========================
# Noise Configuration
# ==========================

NOISE_RATE = 0.05
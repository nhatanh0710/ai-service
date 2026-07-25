from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "datasets" / "task_delay_dataset.csv"


def main():

    df = pd.read_csv(DATASET_PATH)

    print("=" * 60)
    print("DATASET INFORMATION")
    print("=" * 60)

    print(df.info())

    print()

    print("=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)

    print(df.head())

    print()

    print("=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    print(df.isnull().sum())

    print()

    print("=" * 60)
    print("NUMERIC SUMMARY")
    print("=" * 60)

    print(df.describe())

    print()

    print("=" * 60)
    print("RISK DISTRIBUTION")
    print("=" * 60)

    distribution = df["risk"].value_counts()

    percentage = df["risk"].value_counts(normalize=True) * 100

    for risk in distribution.index:

        print(
            f"{risk:<10}"
            f"{distribution[risk]:>6}"
            f" ({percentage[risk]:.2f}%)"
        )

    print()

    print("=" * 60)
    print("VALIDATION")
    print("=" * 60)

    assert (
        df["current_progress"].between(0, 100).all()
    ), "Invalid current_progress"

    assert (
        df["estimate_time"] > 0
    ).all(), "Invalid estimate_time"

    assert (
        df["actual_time"] >= 0
    ).all(), "Invalid actual_time"

    assert (
        df["assignee_count"] >= 1
    ).all(), "Invalid assignee_count"

    assert (
        df["average_workload"] >= 0
    ).all(), "Invalid workload"

    print("Dataset validation passed!")

    print("=" * 60)


if __name__ == "__main__":
    main()
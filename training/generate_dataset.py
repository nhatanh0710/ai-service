import csv

from feature_config import (
    DATASET_SIZE,
    OUTPUT_PATH,
)

from data_generator import (
    generate_priority,
    generate_estimate_time,
    generate_task_complexity,
    generate_assignee_count,
    generate_average_workload,
    generate_remaining_days,
    generate_current_progress,
    generate_actual_time,
)

from risk_rules import (
    calculate_risk_score,
    classify_risk,
    apply_noise,
)


def main():

    statistics = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
    }

    with open(
    OUTPUT_PATH,
    mode="w",
    newline="",
    encoding="utf-8",
) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "priority",
                "estimate_time",
                "actual_time",
                "remaining_days",
                "current_progress",
                "assignee_count",
                "average_workload",
                "task_complexity",
                "risk",
            ]
        )

        for _ in range(DATASET_SIZE):

            priority = generate_priority()

            estimate_time = generate_estimate_time(
                priority
            )

            complexity = generate_task_complexity(
                estimate_time
            )

            assignee_count = generate_assignee_count(
                complexity
            )

            workload = generate_average_workload(
                assignee_count
            )

            remaining_days = generate_remaining_days(
                estimate_time
            )

            progress = generate_current_progress(
                remaining_days,
                workload,
            )

            actual_time = generate_actual_time(
                estimate_time,
                progress,
            )

            score = calculate_risk_score(
                priority,
                estimate_time,
                actual_time,
                remaining_days,
                progress,
                assignee_count,
                workload,
                complexity,
            )

            risk = classify_risk(score)

            risk = apply_noise(risk)

            statistics[risk] += 1

            writer.writerow(
                [
                    priority.value,
                    estimate_time,
                    actual_time,
                    remaining_days,
                    progress,
                    assignee_count,
                    workload,
                    complexity.value,
                    risk,
                ]
            )

    print("=" * 50)
    print("Dataset generated successfully")
    print("=" * 50)
    print(f"Total Records : {DATASET_SIZE}")
    print(f"LOW           : {statistics['LOW']}")
    print(f"MEDIUM        : {statistics['MEDIUM']}")
    print(f"HIGH          : {statistics['HIGH']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
"""Evaluate trained classifiers on the held-out temporal test partition."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from src.models import TrainedClassifiers, train_classifiers
from src.preprocessing import (
    FinalEvaluationSplit,
    TemporalDataSplit,
    load_final_evaluation_split,
)


def binary_metrics(
    labels: pd.Series | np.ndarray, predictions: pd.Series | np.ndarray
) -> dict[str, float]:
    """Calculate binary metrics with malware (1) as the positive class."""
    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(
            labels, predictions, pos_label=1, zero_division=0
        ),
        "recall": recall_score(labels, predictions, pos_label=1, zero_division=0),
        "f1_score": f1_score(labels, predictions, pos_label=1, zero_division=0),
    }


def evaluate_test_set(
    models: TrainedClassifiers,
    split: TemporalDataSplit | FinalEvaluationSplit,
) -> pd.DataFrame:
    """Return pooled and per-year binary metrics, with malware (1) positive."""
    training_years = set(models.training_years)
    test_years = set(split.test_years)
    if training_years & test_years:
        raise ValueError("A model's training years overlap the held-out test years.")
    if not training_years or max(training_years) >= min(test_years):
        raise ValueError("All model training years must precede the test years.")
    if split.y_test.empty or split.y_test.isna().any():
        raise ValueError("Test labels must be present and non-empty.")
    if not split.y_test.isin([0, 1]).all():
        raise ValueError("Test labels must be encoded as 0 or 1.")
    if len(split.year_test) != len(split.y_test):
        raise ValueError("Test year metadata must align with test labels.")
    observed_years = set(int(year) for year in split.year_test.unique())
    if observed_years != test_years:
        raise ValueError(
            "Test year metadata must contain rows for exactly the declared test years."
        )

    named_models = {
        "Logistic Regression": models.logistic_regression,
        "Random Forest": models.random_forest,
    }
    results = []
    for model_name, model in named_models.items():
        predictions = model.predict(split.X_test)
        comparison_groups = [
            (tuple(sorted(test_years)), split.y_test.to_numpy(), predictions)
        ]
        year_values = split.year_test.to_numpy()
        for year in sorted(test_years):
            mask = year_values == year
            comparison_groups.append(
                ((year,), split.y_test.to_numpy()[mask], predictions[mask])
            )

        for years, labels, year_predictions in comparison_groups:
            results.append(
                {
                    "classifier": model_name,
                    "test_rows": len(labels),
                    "test_years": years,
                    "positive_class": 1,
                    "actual_goodware": int((labels == 0).sum()),
                    "actual_malware": int((labels == 1).sum()),
                    "predicted_goodware": int((year_predictions == 0).sum()),
                    "predicted_malware": int((year_predictions == 1).sum()),
                    **binary_metrics(labels, year_predictions),
                }
            )
    return pd.DataFrame(results)


def main() -> None:
    """Train the Step 4 classifiers and report pooled and per-year test metrics."""
    project_root = Path(__file__).resolve().parents[1]
    split = load_final_evaluation_split(project_root / "input_data")
    trained_models = train_classifiers(
        split.X_train,
        split.y_train,
        training_years=split.train_years,
    )
    results = evaluate_test_set(trained_models, split)

    print("Positive class: malware (1)")
    print(f"Test years: {list(split.test_years)}; rows: {len(split.y_test):,}")
    print(
        results[
            [
                "classifier",
                "test_years",
                "test_rows",
                "predicted_goodware",
                "predicted_malware",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
            ]
        ].to_string(index=False, float_format=lambda value: f"{value:.4f}")
    )


if __name__ == "__main__":
    main()

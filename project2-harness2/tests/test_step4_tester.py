from dataclasses import replace

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from src.models import (
    create_classifiers,
    train_classifiers,
    train_from_temporal_split,
)
from src.preprocessing import create_temporal_split


def _training_data():
    return (
        pd.DataFrame(
            {
                "api_a": [-2, -1, 1, 2, -3, -1, 1, 3],
                "api_b": [1, 2, 1, 2, 2, 1, 2, 1],
            }
        ),
        pd.Series([0, 0, 1, 1, 0, 0, 1, 1], name="target"),
    )


def _yearly_data():
    yearly = {}
    for year in range(2014, 2022):
        yearly[year] = pd.DataFrame(
            {
                "api_a": [0, 0, 10, 10],
                "api_b": [1, 2, 1, 2],
                "target": [0, 0, 1, 1],
            }
        )
    return yearly


def test_factory_returns_the_two_planned_classifiers_with_fixed_seed():
    models = create_classifiers()

    assert set(models) == {"logistic_regression", "random_forest"}
    assert isinstance(models["logistic_regression"], LogisticRegression)
    assert isinstance(models["random_forest"], RandomForestClassifier)
    assert models["logistic_regression"].random_state == 42
    assert models["random_forest"].random_state == 42


def test_train_fits_both_models_and_returns_consistent_metadata():
    features, labels = _training_data()
    result = train_classifiers(features, labels, training_years=(2014, 2015))

    assert result.training_years == (2014, 2015)
    assert result.training_rows == len(labels)
    assert result.feature_count == features.shape[1]
    assert result.classes == (0, 1)
    assert set(result.fit_seconds) == {"logistic_regression", "random_forest"}
    assert all(seconds >= 0 for seconds in result.fit_seconds.values())

    for model in (result.logistic_regression, result.random_forest):
        predictions = model.predict(features)
        assert predictions.shape == (len(features),)
        assert set(predictions).issubset({0, 1})
        assert model.n_features_in_ == features.shape[1]


def test_repeated_fits_are_reproducible():
    features, labels = _training_data()
    first = train_classifiers(features, labels, training_years=(2014, 2015))
    second = train_classifiers(features, labels, training_years=(2014, 2015))

    np.testing.assert_array_equal(
        first.logistic_regression.predict(features),
        second.logistic_regression.predict(features),
    )
    np.testing.assert_allclose(
        first.logistic_regression.coef_, second.logistic_regression.coef_
    )
    np.testing.assert_array_equal(
        first.random_forest.predict(features), second.random_forest.predict(features)
    )
    np.testing.assert_allclose(
        first.random_forest.predict_proba(features),
        second.random_forest.predict_proba(features),
    )


def test_temporal_training_uses_only_training_partition():
    first_split = create_temporal_split(_yearly_data())
    altered_holdout_split = replace(
        first_split,
        X_validation=first_split.X_validation + 100_000,
        y_validation=1 - first_split.y_validation,
        X_test=first_split.X_test - 100_000,
        y_test=1 - first_split.y_test,
    )

    first = train_from_temporal_split(first_split)
    altered = train_from_temporal_split(altered_holdout_split)
    probe = first_split.X_train

    assert first.training_years == (2014, 2015, 2016, 2017)
    assert first.training_rows == len(first_split.y_train)
    for name in ("logistic_regression", "random_forest"):
        first_model = getattr(first, name)
        altered_model = getattr(altered, name)
        np.testing.assert_array_equal(
            first_model.predict(probe), altered_model.predict(probe)
        )
        np.testing.assert_allclose(
            first_model.predict_proba(probe), altered_model.predict_proba(probe)
        )


@pytest.mark.parametrize(
    ("features", "labels", "message"),
    [
        (pd.DataFrame(columns=["api_a"]), pd.Series(dtype=int), "must not be empty"),
        (
            pd.DataFrame({"api_a": [0, 1]}),
            pd.Series([0]),
            "equal row counts",
        ),
        (
            pd.DataFrame({"api_a": [0, 1]}),
            pd.Series([0, 2]),
            "encoded as 0 or 1",
        ),
        (
            pd.DataFrame({"api_a": [0, 1]}),
            pd.Series([0, np.nan]),
            "encoded as 0 or 1",
        ),
    ],
)
def test_rejects_empty_or_inconsistent_training_input(features, labels, message):
    with pytest.raises(ValueError, match=message):
        train_classifiers(features, labels, training_years=(2014,))


def test_single_class_training_failure_is_surfaced():
    features = pd.DataFrame({"api_a": [0, 1, 2]})
    labels = pd.Series([0, 0, 0])

    with pytest.raises(ValueError, match="at least 2 classes"):
        train_classifiers(features, labels, training_years=(2014,))

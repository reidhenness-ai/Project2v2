import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.evaluation import evaluate_test_set
from src.models import TrainedClassifiers
from src.preprocessing import TemporalDataSplit


class FixedPredictor:
    def __init__(self, predictions):
        self.predictions = np.asarray(predictions)
        self.seen = []

    def predict(self, features):
        self.seen.append(features.copy())
        return self.predictions


def _test_split(
    y_test=None,
    year_test=None,
    test_years=(2019, 2020, 2021),
):
    if y_test is None:
        y_test = [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1]
    if year_test is None:
        year_test = [2019] * 4 + [2020] * 4 + [2021] * 4
    test_features = pd.DataFrame({"api_signal": np.arange(len(y_test))})
    return TemporalDataSplit(
        X_train=pd.DataFrame({"api_signal": [0.0, 1.0]}),
        y_train=pd.Series([0, 1], name="target"),
        year_train=pd.Series([2014, 2014], name="year"),
        X_validation=pd.DataFrame({"api_signal": [2.0]}),
        y_validation=pd.Series([0], name="target"),
        year_validation=pd.Series([2018], name="year"),
        X_test=test_features,
        y_test=pd.Series(y_test, name="target"),
        year_test=pd.Series(year_test, name="year"),
        scaler=StandardScaler(),
        feature_columns=("api_signal",),
        train_years=(2014, 2015, 2016, 2017),
        validation_years=(2018,),
        test_years=test_years,
    )


def _trained_models(logistic_predictions=None, forest_predictions=None, years=None):
    if logistic_predictions is None:
        logistic_predictions = [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]
    if forest_predictions is None:
        forest_predictions = [0] * len(logistic_predictions)
    if years is None:
        years = (2014, 2015, 2016, 2017)
    return TrainedClassifiers(
        logistic_regression=FixedPredictor(logistic_predictions),
        random_forest=FixedPredictor(forest_predictions),
        training_years=years,
        training_rows=8,
        feature_count=1,
        classes=(0, 1),
        fit_seconds={"logistic_regression": 0.0, "random_forest": 0.0},
    )


def test_computes_pooled_metrics_with_malware_as_positive_class():
    split = _test_split()
    models = _trained_models()

    results = evaluate_test_set(models, split)

    logistic = results.loc[
        (results["classifier"] == "Logistic Regression")
        & (results["test_rows"] == 12)
    ].iloc[0]
    assert logistic["test_rows"] == 12
    assert logistic["test_years"] == (2019, 2020, 2021)
    assert logistic["positive_class"] == 1
    assert logistic["accuracy"] == pytest.approx(9 / 12)
    assert logistic["precision"] == pytest.approx(5 / 6)
    assert logistic["recall"] == pytest.approx(5 / 7)
    assert logistic["f1_score"] == pytest.approx(10 / 13)

    forest = results.loc[
        (results["classifier"] == "Random Forest") & (results["test_rows"] == 12)
    ].iloc[0]
    assert forest["accuracy"] == pytest.approx(5 / 12)
    assert forest["precision"] == 0
    assert forest["recall"] == 0
    assert forest["f1_score"] == 0

    pd.testing.assert_frame_equal(models.logistic_regression.seen[0], split.X_test)
    pd.testing.assert_frame_equal(models.random_forest.seen[0], split.X_test)


def test_returns_metrics_for_each_test_year_and_for_the_pooled_test_set():
    results = evaluate_test_set(_trained_models(), _test_split())

    assert set(results["classifier"]) == {"Logistic Regression", "Random Forest"}
    assert len(results) == 2 * 4
    year_groups = set(results["test_years"])
    assert year_groups == {
        (2019,),
        (2020,),
        (2021,),
        (2019, 2020, 2021),
    }


def test_zero_division_is_defined_when_predictions_have_no_malware():
    split = _test_split(
        y_test=[0, 1, 0, 1],
        year_test=[2019, 2019, 2020, 2020],
        test_years=(2019, 2020),
    )
    models = _trained_models(
        logistic_predictions=[0, 0, 0, 0],
        forest_predictions=[0, 0, 0, 0],
    )

    results = evaluate_test_set(models, split)

    assert (results["precision"] == 0).all()
    assert (results["recall"] == 0).all()
    assert (results["f1_score"] == 0).all()


@pytest.mark.parametrize(
    ("training_years", "test_years", "message"),
    [
        ((2014, 2019), (2019, 2020), "overlap"),
        ((2014, 2020), (2019, 2021), "precede"),
        ((), (2019, 2020), "precede"),
    ],
)
def test_rejects_training_test_year_overlap_or_nonchronological_fit(
    training_years, test_years, message
):
    with pytest.raises(ValueError, match=message):
        evaluate_test_set(
            _trained_models(years=training_years),
            _test_split(test_years=test_years),
        )


@pytest.mark.parametrize(
    ("labels", "message"),
    [
        ([], "present and non-empty"),
        ([0, 1, np.nan, 0], "present and non-empty"),
        ([0, 1, 2, 0], "encoded as 0 or 1"),
    ],
)
def test_rejects_empty_missing_or_invalid_test_labels(labels, message):
    split = _test_split(
        y_test=labels,
        year_test=[2019] * len(labels),
        test_years=(2019,),
    )
    models = _trained_models(
        logistic_predictions=[0] * len(labels),
        forest_predictions=[0] * len(labels),
    )

    with pytest.raises(ValueError, match=message):
        evaluate_test_set(models, split)

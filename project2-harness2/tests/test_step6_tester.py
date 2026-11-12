import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.evaluation import evaluate_test_set
from src.models import TrainedClassifiers, train_classifiers
from src.preprocessing import FinalEvaluationSplit, load_final_evaluation_split


class FixedPredictor:
    def __init__(self, predictions):
        self.predictions = np.asarray(predictions)
        self.seen = []

    def predict(self, features):
        self.seen.append(features.copy())
        return self.predictions


def _final_split(y_test=None, year_test=None, test_years=(2019, 2020, 2021)):
    if y_test is None:
        y_test = [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1]
    if year_test is None:
        year_test = [2019] * 4 + [2020] * 4 + [2021] * 4
    return FinalEvaluationSplit(
        X_train=pd.DataFrame({"api_signal": [0.0, 1.0]}),
        y_train=pd.Series([0, 1], name="target"),
        year_train=pd.Series([2014, 2018], name="year"),
        X_test=pd.DataFrame({"api_signal": np.arange(len(y_test))}),
        y_test=pd.Series(y_test, name="target"),
        year_test=pd.Series(year_test, name="year"),
        scaler=StandardScaler(),
        feature_columns=("api_signal",),
        train_years=(2014, 2015, 2016, 2017, 2018),
        test_years=test_years,
    )


def _models():
    logistic_predictions = [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]
    forest_predictions = [0] * len(logistic_predictions)
    return TrainedClassifiers(
        logistic_regression=FixedPredictor(logistic_predictions),
        random_forest=FixedPredictor(forest_predictions),
        training_years=(2014, 2015, 2016, 2017, 2018),
        training_rows=10,
        feature_count=1,
        classes=(0, 1),
        fit_seconds={"logistic_regression": 0.0, "random_forest": 0.0},
    )


def test_outputs_each_classifier_by_year_and_pooled_with_correct_counts_and_metrics():
    split = _final_split()
    models = _models()

    results = evaluate_test_set(models, split)

    assert len(results) == 2 * 4
    assert set(results["classifier"]) == {"Logistic Regression", "Random Forest"}
    assert set(results["test_years"]) == {
        (2019,),
        (2020,),
        (2021,),
        (2019, 2020, 2021),
    }
    assert (results["positive_class"] == 1).all()
    assert (results["actual_goodware"] + results["actual_malware"] == results["test_rows"]).all()
    assert (results["predicted_goodware"] + results["predicted_malware"] == results["test_rows"]).all()

    logistic = results.loc[results["classifier"] == "Logistic Regression"]
    logistic_2019 = logistic.loc[logistic["test_years"] == (2019,)].iloc[0]
    assert logistic_2019["test_rows"] == 4
    assert logistic_2019["actual_goodware"] == 2
    assert logistic_2019["actual_malware"] == 2
    assert logistic_2019["predicted_goodware"] == 3
    assert logistic_2019["predicted_malware"] == 1
    assert logistic_2019["accuracy"] == pytest.approx(3 / 4)
    assert logistic_2019["precision"] == pytest.approx(1)
    assert logistic_2019["recall"] == pytest.approx(1 / 2)
    assert logistic_2019["f1_score"] == pytest.approx(2 / 3)

    pooled = logistic.loc[logistic["test_rows"] == 12].iloc[0]
    assert pooled["test_years"] == (2019, 2020, 2021)
    assert pooled["actual_goodware"] == 5
    assert pooled["actual_malware"] == 7
    assert pooled["predicted_goodware"] == 6
    assert pooled["predicted_malware"] == 6
    assert pooled["accuracy"] == pytest.approx(9 / 12)
    assert pooled["precision"] == pytest.approx(5 / 6)
    assert pooled["recall"] == pytest.approx(5 / 7)
    assert pooled["f1_score"] == pytest.approx(10 / 13)

    pd.testing.assert_frame_equal(models.logistic_regression.seen[0], split.X_test)
    pd.testing.assert_frame_equal(models.random_forest.seen[0], split.X_test)


def test_final_loader_fits_on_2014_through_2018_and_keeps_later_years_held_out(
    tmp_path,
):
    for year in range(2014, 2022):
        for class_name, label in (("benign", 0), ("malware", 1)):
            path = tmp_path / f"sampled_{year}_{class_name}_api.csv"
            pd.DataFrame(
                {
                    "apkname": [f"{year}-{class_name}-a", f"{year}-{class_name}-b"],
                    "api_a": [year * 10_000, year * 10_000 + 2],
                    "api_b": [label * 10, label * 10 + 2],
                }
            ).to_csv(path, index=False)

    split = load_final_evaluation_split(tmp_path)

    assert split.train_years == (2014, 2015, 2016, 2017, 2018)
    assert split.test_years == (2019, 2020, 2021)
    assert set(split.year_train) == set(split.train_years)
    assert set(split.year_test) == set(split.test_years)
    assert split.X_train.shape == (20, 2)
    assert split.X_test.shape == (12, 2)
    assert split.scaler.n_samples_seen_ == 20
    assert split.feature_columns == ("api_a", "api_b")
    np.testing.assert_allclose(split.scaler.mean_, [20_160_001, 6])
    assert split.y_train.value_counts().to_dict() == {0: 10, 1: 10}
    assert split.y_test.value_counts().to_dict() == {0: 6, 1: 6}
    assert split.year_test.value_counts().to_dict() == {
        2019: 4,
        2020: 4,
        2021: 4,
    }

    models = train_classifiers(
        split.X_train,
        split.y_train,
        training_years=split.train_years,
    )
    results = evaluate_test_set(models, split)
    assert results.groupby("classifier").size().to_dict() == {
        "Logistic Regression": 4,
        "Random Forest": 4,
    }
    assert set(results["test_years"]) == {
        (2019,),
        (2020,),
        (2021,),
        (2019, 2020, 2021),
    }
    for metric in ("accuracy", "precision", "recall", "f1_score"):
        assert np.isfinite(results[metric]).all()
        assert results[metric].between(0, 1).all()
    assert (
        results["predicted_goodware"] + results["predicted_malware"]
        == results["test_rows"]
    ).all()


@pytest.mark.parametrize(
    ("year_test", "message"),
    [
        ([2019] * 11, "metadata must align"),
        ([2019] * 4 + [2020] * 8, "exactly the declared test years"),
        ([2018] * 4 + [2020] * 4 + [2021] * 4, "exactly the declared test years"),
    ],
)
def test_rejects_misaligned_or_incomplete_test_year_metadata(year_test, message):
    split = _final_split(year_test=year_test)
    with pytest.raises(ValueError, match=message):
        evaluate_test_set(_models(), split)


def test_rejects_model_trained_on_a_test_year():
    split = _final_split()
    models = _models()
    models.training_years = (2014, 2015, 2019)

    with pytest.raises(ValueError, match="overlap"):
        evaluate_test_set(models, split)

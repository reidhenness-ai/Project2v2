import numpy as np
import pandas as pd

from src.sustainable import compare_retraining_strategies


def _write_dataset(directory):
    for year in range(2014, 2022):
        for class_name, label in (("benign", 0), ("malware", 1)):
            path = directory / f"sampled_{year}_{class_name}_api.csv"
            offsets = np.arange(4)
            pd.DataFrame(
                {
                    "apkname": [f"{year}-{class_name}-{index}" for index in offsets],
                    "api_class": label * 10 + offsets,
                    "api_time": year - 2014 + offsets,
                }
            ).to_csv(path, index=False)


def test_comparison_uses_expanding_training_windows_and_matching_test_years(tmp_path):
    _write_dataset(tmp_path)

    results = compare_retraining_strategies(tmp_path)

    assert len(results) == 12
    assert set(results["approach"]) == {"Static baseline", "Periodic retraining"}
    assert set(results["classifier"]) == {"Logistic Regression", "Random Forest"}
    assert set(results["test_year"]) == {2019, 2020, 2021}
    assert len(results.groupby(["approach", "classifier", "test_year"])) == 12

    expected_training_years = {
        ("Static baseline", 2019): (2014, 2015, 2016, 2017, 2018),
        ("Static baseline", 2020): (2014, 2015, 2016, 2017, 2018),
        ("Static baseline", 2021): (2014, 2015, 2016, 2017, 2018),
        ("Periodic retraining", 2019): (2014, 2015, 2016, 2017, 2018),
        ("Periodic retraining", 2020): (2014, 2015, 2016, 2017, 2018, 2019),
        (
            "Periodic retraining",
            2021,
        ): (2014, 2015, 2016, 2017, 2018, 2019, 2020),
    }
    expected_training_rows = {
        (2014, 2015, 2016, 2017, 2018): 40,
        (2014, 2015, 2016, 2017, 2018, 2019): 48,
        (2014, 2015, 2016, 2017, 2018, 2019, 2020): 56,
    }

    for row in results.itertuples(index=False):
        expected_years = expected_training_years[(row.approach, row.test_year)]
        assert row.training_years == expected_years
        assert max(row.training_years) < row.test_year
        assert row.training_rows == expected_training_rows[expected_years]
        assert row.test_rows == 8
        assert row.positive_class == 1
        assert row.predicted_goodware + row.predicted_malware == row.test_rows
        assert 0 <= row.accuracy <= 1
        assert 0 <= row.precision <= 1
        assert 0 <= row.recall <= 1
        assert 0 <= row.f1_score <= 1


def test_first_year_baseline_and_retraining_results_are_identical(tmp_path):
    _write_dataset(tmp_path)

    results = compare_retraining_strategies(tmp_path)
    for classifier in ("Logistic Regression", "Random Forest"):
        rows = results.loc[
            (results["classifier"] == classifier) & (results["test_year"] == 2019)
        ]
        baseline = rows.loc[rows["approach"] == "Static baseline"].drop(
            columns="approach"
        ).iloc[0]
        retrained = rows.loc[rows["approach"] == "Periodic retraining"].drop(
            columns="approach"
        ).iloc[0]
        pd.testing.assert_series_equal(
            baseline,
            retrained,
            check_names=False,
        )

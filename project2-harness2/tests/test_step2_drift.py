import numpy as np
import pandas as pd
import pytest

from src.drift import (
    _benjamini_hochberg,
    _build_report,
    _format_p_value,
    compare_years_to_reference,
)


def _year_frame(feature_a, feature_b, target):
    return pd.DataFrame(
        {"api_a": feature_a, "api_b": feature_b, "target": target}
    )


def test_identical_distributions_have_zero_ks_and_no_significance():
    rows = _year_frame([0, 0, 1, 1], [4, 4, 4, 4], [0, 0, 1, 1])

    results = compare_years_to_reference({2014: rows, 2015: rows.copy()})

    assert len(results) == 6
    assert (results["ks_statistic"] == 0).all()
    assert (results["p_value"] == 1).all()
    assert not results["significant"].any()


def test_detects_shifted_features_within_each_class():
    reference = _year_frame(
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1],
    )
    comparison = _year_frame(
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 9, 9, 9, 9],
        [0, 0, 0, 0, 1, 1, 1, 1],
    )

    results = compare_years_to_reference(
        {2014: reference, 2015: comparison}, alpha=0.05
    )

    malware_feature = results.loc[
        (results["scope"] == "malware") & (results["feature"] == "api_b")
    ].iloc[0]
    goodware_feature = results.loc[
        (results["scope"] == "goodware") & (results["feature"] == "api_b")
    ].iloc[0]
    assert malware_feature["ks_statistic"] == 1
    assert malware_feature["significant"]
    assert goodware_feature["ks_statistic"] == 0
    assert not goodware_feature["significant"]


def test_benjamini_hochberg_adjustment_is_monotone_in_rank():
    adjusted = _benjamini_hochberg(np.array([0.01, 0.04, 0.03]))

    np.testing.assert_allclose(adjusted, [0.03, 0.04, 0.04])


def test_underflowed_p_values_are_not_reported_as_exact_zero():
    assert _format_p_value(0.0) == "<1e-300"


def test_report_ranks_years_by_mean_ks_and_formats_underflowed_p_values():
    rows = []
    for scope in ("overall", "goodware", "malware"):
        for year, ks_value in ((2015, 0.25), (2016, 0.75)):
            for feature in ("api_a", "api_b"):
                rows.append(
                    {
                        "reference_year": 2014,
                        "comparison_year": year,
                        "scope": scope,
                        "feature": feature,
                        "ks_statistic": ks_value,
                        "p_value": 0.0,
                        "q_value": 0.0,
                        "significant": True,
                    }
                )

    report = _build_report(pd.DataFrame(rows), alpha=0.05)

    assert "Ranked by mean feature-wise KS statistic" in report
    assert report.index("| overall | 2016 |") < report.index("| overall | 2015 |")
    assert "<1e-300" in report


@pytest.mark.parametrize("p_values", [np.array([-0.1, 0.5]), np.array([0.2, np.nan])])
def test_rejects_invalid_p_values(p_values):
    with pytest.raises(ValueError):
        _benjamini_hochberg(p_values)


def test_rejects_feature_schema_mismatch():
    first = _year_frame([0, 1], [0, 1], [0, 1])
    second = pd.DataFrame({"other": [0, 1], "api_b": [0, 1], "target": [0, 1]})

    with pytest.raises(ValueError, match="Feature schema mismatch"):
        compare_years_to_reference({2014: first, 2015: second})

import numpy as np
import pandas as pd
import pytest
from scipy.stats import ks_2samp

import src.drift as drift
from src.drift import compare_years_to_reference, write_drift_report


def _frame(features, target):
    return pd.DataFrame({**features, "target": target})


def _expected_bh(p_values):
    p_values = np.asarray(p_values, dtype=float)
    order = np.argsort(p_values)
    ranked = p_values[order] * len(p_values) / np.arange(1, len(p_values) + 1)
    adjusted = np.minimum.accumulate(ranked[::-1])[::-1].clip(max=1.0)
    result = np.empty_like(adjusted)
    result[order] = adjusted
    return result


def test_compares_each_feature_to_reference_for_each_later_year_and_scope():
    reference = _frame(
        {"api_a": [0, 1, 0, 1], "api_b": [5, 5, 6, 6]},
        [0, 0, 1, 1],
    )
    later = _frame(
        {"api_a": [0, 1, 1, 1], "api_b": [5, 5, 6, 6]},
        [0, 0, 1, 1],
    )

    results = compare_years_to_reference(
        {2014: reference, 2015: later, 2016: later.copy()}
    )

    assert len(results) == 2 * 3 * 2
    assert set(results["reference_year"]) == {2014}
    assert set(results["comparison_year"]) == {2015, 2016}
    assert set(results["scope"]) == {"overall", "goodware", "malware"}
    assert set(results["feature"]) == {"api_a", "api_b"}
    assert not (results["comparison_year"] == 2014).any()
    assert results["ks_statistic"].between(0, 1).all()
    assert results["p_value"].between(0, 1).all()
    assert results["q_value"].between(0, 1).all()


def test_ks_statistic_and_p_value_match_two_sided_scipy_test():
    reference = _frame(
        {"api_a": [0, 0, 0, 0, 1, 1, 1, 1], "api_b": [1, 2, 1, 2, 1, 2, 1, 2]},
        [0, 0, 0, 0, 1, 1, 1, 1],
    )
    comparison = _frame(
        {"api_a": [0, 0, 0, 0, 2, 2, 2, 2], "api_b": [1, 2, 1, 2, 1, 2, 1, 2]},
        [0, 0, 0, 0, 1, 1, 1, 1],
    )

    result = compare_years_to_reference(
        {2014: reference, 2015: comparison}
    ).query("scope == 'overall' and feature == 'api_a'").iloc[0]
    expected = ks_2samp(
        reference["api_a"],
        comparison["api_a"],
        alternative="two-sided",
        method="asymp",
    )

    assert result["ks_statistic"] == pytest.approx(expected.statistic)
    assert result["p_value"] == pytest.approx(expected.pvalue)


def test_class_stratification_separates_class_mix_change_from_feature_drift():
    reference = _frame(
        {"api_calls": [0] * 10 + [1] * 10},
        [0] * 10 + [1] * 10,
    )
    comparison = _frame(
        {"api_calls": [0] * 18 + [1] * 2},
        [0] * 18 + [1] * 2,
    )

    results = compare_years_to_reference(
        {2014: reference, 2015: comparison}
    ).set_index("scope")

    assert results.loc["overall", "ks_statistic"] == pytest.approx(0.4)
    assert results.loc["goodware", "ks_statistic"] == 0
    assert results.loc["malware", "ks_statistic"] == 0


def test_bh_adjustment_is_applied_per_scope_and_comparison_year():
    target = [0, 1] * 20
    reference = _frame(
        {
            "same": [0] * 40,
            "partial": [0] * 40,
            "shifted": [0] * 40,
        },
        target,
    )
    comparison = _frame(
        {
            "same": [0] * 40,
            "partial": [0] * 20 + [1] * 20,
            "shifted": [1] * 40,
        },
        target,
    )

    results = compare_years_to_reference(
        {2014: reference, 2015: comparison}
    )
    for scope in ("overall", "goodware", "malware"):
        scoped = results.loc[results["scope"] == scope]
        expected = _expected_bh(scoped["p_value"].to_numpy())
        np.testing.assert_allclose(scoped["q_value"].to_numpy(), expected)
        assert (
            scoped.sort_values("p_value")["q_value"].diff().dropna() >= -1e-15
        ).all()


def test_analysis_does_not_mutate_input_frames():
    reference = _frame({"api_a": [0, 1, 0, 1]}, [0, 0, 1, 1])
    comparison = _frame({"api_a": [1, 1, 0, 0]}, [0, 0, 1, 1])
    original_reference = reference.copy(deep=True)
    original_comparison = comparison.copy(deep=True)

    compare_years_to_reference({2014: reference, 2015: comparison})

    pd.testing.assert_frame_equal(reference, original_reference)
    pd.testing.assert_frame_equal(comparison, original_comparison)


@pytest.mark.parametrize("alpha", [0, 1, -0.1, 1.1, float("nan")])
def test_rejects_alpha_outside_open_unit_interval(alpha):
    frame = _frame({"api_a": [0, 1]}, [0, 1])

    with pytest.raises(ValueError, match="alpha"):
        compare_years_to_reference({2014: frame, 2015: frame.copy()}, alpha=alpha)


def test_rejects_missing_reference_or_missing_comparison_year():
    frame = _frame({"api_a": [0, 1]}, [0, 1])

    with pytest.raises(ValueError, match="Reference year 2013"):
        compare_years_to_reference({2014: frame, 2015: frame.copy()}, 2013)
    with pytest.raises(ValueError, match="At least one comparison year"):
        compare_years_to_reference({2014: frame}, 2014)


@pytest.mark.parametrize(
    ("reference", "comparison", "message"),
    [
        (
            pd.DataFrame({"api_a": [0, 1]}),
            _frame({"api_a": [0, 1]}, [0, 1]),
            "target",
        ),
        (
            _frame({"api_a": [0, 1]}, [0, 1]),
            _frame({"other": [0, 1]}, [0, 1]),
            "Feature schema mismatch",
        ),
        (
            _frame({"api_a": [0, 1]}, [0, 1]),
            _frame({"api_a": [0, np.nan]}, [0, 1]),
            "missing feature values",
        ),
        (
            _frame({"api_a": [0, 1]}, [0, 1]),
            _frame({"api_a": [0, np.inf]}, [0, 1]),
            "non-finite",
        ),
        (
            _frame({"api_a": [0, 1]}, [0, 1]),
            _frame({"api_a": [0, 1]}, [0, 2]),
            "target values must be 0 or 1",
        ),
    ],
)
def test_rejects_invalid_year_frames(reference, comparison, message):
    with pytest.raises(ValueError, match=message):
        compare_years_to_reference({2014: reference, 2015: comparison})


def test_rejects_year_missing_one_of_the_class_labels():
    reference = _frame({"api_a": [0, 1]}, [0, 1])
    comparison = _frame({"api_a": [0, 0]}, [0, 0])

    with pytest.raises(ValueError, match="Both years must contain target 1"):
        compare_years_to_reference({2014: reference, 2015: comparison})


def test_report_writer_uses_supplied_analysis_data_and_writes_report(
    tmp_path, monkeypatch
):
    reference = _frame({"api_a": [0, 0, 1, 1]}, [0, 0, 1, 1])
    later = _frame({"api_a": [0, 0, 2, 2]}, [0, 0, 1, 1])
    monkeypatch.setattr(
        drift,
        "load_yearly_data",
        lambda data_dir: {2014: reference, 2015: later},
    )
    report_path = tmp_path / "nested" / "drift.md"

    results = write_drift_report(tmp_path, report_path)

    assert len(results) == 3
    report = report_path.read_text(encoding="utf-8")
    assert "Kolmogorov-Smirnov" in report
    assert "## Years that differ most from 2014" in report
    assert "| overall | 2015 |" in report
    assert "## Features with the largest drift" in report
    assert "## Interpretation and limitations" in report

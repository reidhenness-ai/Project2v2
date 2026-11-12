"""Statistical analysis of API-feature distribution drift across years."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from src.data import load_yearly_data


_CLASS_SCOPES = {"overall": None, "goodware": 0, "malware": 1}


def _benjamini_hochberg(p_values: np.ndarray) -> np.ndarray:
    """Adjust a vector of p-values with the Benjamini-Hochberg procedure."""
    p_values = np.asarray(p_values, dtype=float)
    if p_values.ndim != 1 or not np.isfinite(p_values).all():
        raise ValueError("p_values must be a one-dimensional array of finite values.")
    if ((p_values < 0) | (p_values > 1)).any():
        raise ValueError("p_values must be between 0 and 1.")
    if p_values.size == 0:
        return p_values.copy()

    order = np.argsort(p_values)
    ranked = p_values[order] * p_values.size / np.arange(1, p_values.size + 1)
    adjusted_sorted = np.minimum.accumulate(ranked[::-1])[::-1]
    adjusted = np.empty_like(adjusted_sorted)
    adjusted[order] = np.minimum(adjusted_sorted, 1.0)
    return adjusted


def _format_p_value(value: float) -> str:
    return "<1e-300" if value == 0 else f"{value:.3g}"


def _validated_features(
    data_by_year: dict[int, pd.DataFrame],
) -> tuple[list[int], list[str]]:
    if not data_by_year:
        raise ValueError("At least one year's data is required.")

    years = sorted(data_by_year)
    first = data_by_year[years[0]]
    if "target" not in first.columns:
        raise ValueError(f"Year {years[0]} data must contain a 'target' column.")
    feature_columns = [column for column in first.columns if column != "target"]
    if not feature_columns:
        raise ValueError("At least one feature column is required.")

    for year in years:
        frame = data_by_year[year]
        if "target" not in frame.columns:
            raise ValueError(f"Year {year} data must contain a 'target' column.")
        if [column for column in frame.columns if column != "target"] != feature_columns:
            raise ValueError(f"Feature schema mismatch in year {year}.")
        if frame.empty:
            raise ValueError(f"Year {year} contains no rows.")
        if frame["target"].isna().any() or not frame["target"].isin([0, 1]).all():
            raise ValueError(f"Year {year} target values must be 0 or 1.")
        features = frame[feature_columns]
        if features.isna().any().any():
            raise ValueError(f"Year {year} contains missing feature values.")
        try:
            values = features.to_numpy(dtype=np.float64)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Year {year} contains non-numeric features.") from exc
        if not np.isfinite(values).all():
            raise ValueError(f"Year {year} contains non-finite features.")

    return years, feature_columns


def compare_years_to_reference(
    data_by_year: dict[int, pd.DataFrame],
    reference_year: int = 2014,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Compare every later year's feature distributions to a reference year.

    Runs two-sided, asymptotic two-sample KS tests for every feature, both on
    pooled rows and separately for goodware and malware. Benjamini-Hochberg
    correction is applied across features within each year and class scope.
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")
    years, feature_columns = _validated_features(data_by_year)
    if reference_year not in data_by_year:
        raise ValueError(f"Reference year {reference_year} is not available.")
    comparison_years = [year for year in years if year != reference_year]
    if not comparison_years:
        raise ValueError("At least one comparison year besides the reference is required.")

    results: list[pd.DataFrame] = []
    reference = data_by_year[reference_year]
    for year in comparison_years:
        comparison = data_by_year[year]
        for scope, label in _CLASS_SCOPES.items():
            if label is None:
                reference_rows = reference
                comparison_rows = comparison
            else:
                reference_rows = reference.loc[reference["target"] == label]
                comparison_rows = comparison.loc[comparison["target"] == label]
                if reference_rows.empty or comparison_rows.empty:
                    raise ValueError(
                        f"Both years must contain target {label} for {scope} "
                        f"comparison ({reference_year} vs {year})."
                    )

            reference_values = reference_rows[feature_columns].to_numpy(
                dtype=np.float64, copy=False
            )
            comparison_values = comparison_rows[feature_columns].to_numpy(
                dtype=np.float64, copy=False
            )
            statistics = np.empty(len(feature_columns), dtype=float)
            p_values = np.empty(len(feature_columns), dtype=float)
            for index in range(len(feature_columns)):
                test = ks_2samp(
                    reference_values[:, index],
                    comparison_values[:, index],
                    alternative="two-sided",
                    method="asymp",
                )
                statistics[index] = test.statistic
                p_values[index] = test.pvalue

            q_values = _benjamini_hochberg(p_values)
            results.append(
                pd.DataFrame(
                    {
                        "reference_year": reference_year,
                        "comparison_year": year,
                        "scope": scope,
                        "feature": feature_columns,
                        "ks_statistic": statistics,
                        "p_value": p_values,
                        "q_value": q_values,
                        "significant": q_values <= alpha,
                    }
                )
            )

    return pd.concat(results, ignore_index=True)


def _build_report(results: pd.DataFrame, alpha: float) -> str:
    lines = [
        "# Step 2 Report: Data Drift Analysis",
        "",
        "## Method",
        "",
        "The reproducible analysis in [`src/drift.py`](../src/drift.py) compares "
        "each year from 2015-2021 with 2014, separately for pooled apps, "
        "goodware, and malware. It runs a two-sided, two-sample Kolmogorov-Smirnov "
        "(KS) test on each of the 1,848 API-call features. The KS statistic is "
        "the maximum absolute difference between the two empirical cumulative "
        "distribution functions (an effect size from 0 to 1).",
        "",
        "P-values use SciPy's asymptotic method. Benjamini-Hochberg false "
        "discovery rate correction is performed over the 1,848 feature tests "
        "within each comparison year and scope. Adjusted p-values (`q`) at or "
        f"below {alpha:g} are called significant. The yearly drift ranking uses "
        "mean KS statistic across features, rather than p-values alone, so "
        "large sample sizes do not define practical importance. Inputs are "
        "validated through the Step 1 loader. Values that underflow to zero are "
        "displayed as `<1e-300`. No random sampling or fitting is used.",
        "",
        "Reproduce from the project directory with:",
        "",
        "```bash",
        "python -m src.drift",
        "```",
        "",
        "## Years that differ most from 2014",
        "",
        "Ranked by mean feature-wise KS statistic (largest first). Significant "
        "features are those passing the within-comparison Benjamini-Hochberg "
        "correction.",
        "",
        "| Scope | Year | Median KS | Mean KS | Max KS | Significant features |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    year_summary = (
        results.groupby(["scope", "comparison_year"], as_index=False)
        .agg(
            median_ks=("ks_statistic", "median"),
            mean_ks=("ks_statistic", "mean"),
            max_ks=("ks_statistic", "max"),
            significant_features=("significant", "sum"),
        )
        .sort_values(["scope", "mean_ks"], ascending=[True, False])
    )
    for row in year_summary.itertuples(index=False):
        lines.append(
            f"| {row.scope} | {row.comparison_year} | {row.median_ks:.6f} | "
            f"{row.mean_ks:.6f} | {row.max_ks:.4f} | "
            f"{row.significant_features:,} / 1,848 |"
        )

    lines.extend(
        [
            "",
            "## Features with the largest drift",
            "",
            "For each scope, features are ranked by their maximum KS statistic "
            "across the seven comparisons. The listed year is where that maximum "
            "occurred; `q` is its adjusted p-value for that year and scope.",
        ]
    )
    for scope in ("overall", "goodware", "malware"):
        scope_results = results.loc[results["scope"] == scope]
        peak_indices = scope_results.groupby("feature")["ks_statistic"].idxmax()
        top_features = (
            scope_results.loc[peak_indices]
            .sort_values(["ks_statistic", "q_value"], ascending=[False, True])
            .head(10)
        )
        lines.extend(
            [
                "",
                f"### {scope.title()}",
                "",
                "| Feature | Year | KS statistic | Raw p-value | Adjusted q-value |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for row in top_features.itertuples(index=False):
            lines.append(
                f"| `{row.feature}` | {row.comparison_year} | "
                f"{row.ks_statistic:.4f} | "
                f"{_format_p_value(row.p_value)} | "
                f"{_format_p_value(row.q_value)} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation and limitations",
            "",
            "The tests quantify feature-distribution drift relative to 2014; "
            "they do not establish concept drift or show that a model's "
            "predictive accuracy changed. The class-specific results help "
            "separate within-class feature changes from changes in the pooled "
            "distribution. API-call counts are discrete and tied, whereas the "
            "classical KS p-value calibration assumes continuous distributions; "
            "interpret p-values cautiously and use KS statistics as descriptive "
            "effect sizes. The asymptotic approximation and correction method "
            "are fixed in code for reproducibility.",
            "",
        ]
    )
    return "\n".join(lines)


def write_drift_report(
    data_dir: str | Path,
    report_path: str | Path,
    reference_year: int = 2014,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Analyze the supplied dataset and write the generated Markdown report."""
    data_by_year = load_yearly_data(data_dir)
    results = compare_years_to_reference(
        data_by_year, reference_year=reference_year, alpha=alpha
    )
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_build_report(results, alpha), encoding="utf-8")
    return results


def main() -> None:
    """Generate the Step 2 report using paths relative to the project root."""
    project_root = Path(__file__).resolve().parents[1]
    output = write_drift_report(
        project_root / "input_data",
        project_root / "docs" / "step2_drift_analysis.md",
    )
    print(
        f"Wrote docs/step2_drift_analysis.md with {len(output):,} feature tests "
        f"across {output['comparison_year'].nunique()} year comparisons and "
        f"{output['scope'].nunique()} scopes."
    )


if __name__ == "__main__":
    main()

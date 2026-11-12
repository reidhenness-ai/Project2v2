# Project 2: Malware Classification Under Data Drift

This project uses machine learning to classify Android applications as malware or goodware based on their API-call features. It uses Logistic Regression and Random Forest to evaluate classification performance and analyze how data drift affects predictions over time. The results show that periodically retraining models with newer data can greatly improve performance compared with keeping models unchanged.

This repository was built with the Project 2 harness. See `HARNESS.md` for how the builder, reviewer, and tester agents were run.

## Agents used

| Role | Tool | Model |
|---|---|---|
| Builder | GitHub Copilot (agent mode) | Not recorded |
| Reviewer | GitHub Copilot (agent mode) | Not recorded |
| Tester | GitHub Copilot (agent mode) | Not recorded |

Each agent was run in a separate session with a different responsibility. The builder implemented the code, the reviewer inspected the changes, and the tester independently wrote and ran tests. The saved transcripts do not record the model names.

## How to run

Use Python 3.9 or newer. From this directory, install the required packages:

```bash
python -m pip install -r requirements.txt
```

Place the 16 supplied dataset CSV files in the `input_data/` folder. This folder is excluded from Git, so the data is not committed.

Run the evaluation and periodic-retraining comparison from this directory:

```bash
python -m src.evaluation
python -m src.sustainable
```

These commands print their results. The corresponding reports are documented in `docs/`; there is not currently a single `src.main` command that runs every project step.

Run all tests:

```bash
python harness.py test all
```

To run tests for one step, use `python harness.py test N`, where `N` is 1 through 7.

## Results

The project evaluated Logistic Regression and Random Forest using accuracy, precision, recall, and F1-score. On the combined 2019–2021 test set, Logistic Regression achieved 56.40% accuracy and a 0.6931 F1-score. Random Forest achieved 54.17% accuracy and a 0.6837 F1-score.

The data drift analysis found increasing feature distribution differences over time. Random Forest performance declined across the test years, while Logistic Regression showed some variation.

The sustainable machine learning comparison showed that periodic retraining performed better than keeping the original models unchanged. By 2021, retrained Logistic Regression achieved 90.03% accuracy, and retrained Random Forest achieved 94.17% accuracy.

For more detailed results, see:

- [`docs/step5_evaluation.md`](docs/step5_evaluation.md) - Classifier evaluation and metric comparisons.
- [`docs/step6_test_results.md`](docs/step6_test_results.md) - Per-year predictions, performance, and data drift observations.
- [`docs/step7_sustainable_approach.md`](docs/step7_sustainable_approach.md) - Comparison of static models and periodic retraining.

## Hand-written code

No Python implementation code was written by hand; the implementation was written and edited by the builder agent. The student directed the agents, wrote and revised prompts, reviewed their feedback, and made decisions about which changes were necessary.

# Data Science Tool Mastery Project

A portfolio of practical exercises across the industry-standard data science toolchain, built around one coherent problem: **predicting diabetes disease progression from baseline measurements** (real clinical data, 442 patients).

> Educational project. The model is **not** a clinical tool.

## Objectives and how they are met

| # | Objective | How |
|---|---|---|
| 1 | Master industry-standard tools | Git, NumPy, Pandas, SQL (SQLite), Matplotlib, Seaborn, SciPy, Scikit-learn, joblib, unittest, each used for what it does best |
| 2 | Demonstrate proficiency through practical exercises | Every exercise runs, shows real output, and is **cross-checked** with a second tool or an automated test |
| 3 | Create portfolio pieces | A tested Python package, a SQL analytics script, a saved model with a model card, a chart gallery and a documented notebook |

## Portfolio pieces

| Piece | Location | What it shows |
|---|---|---|
| Tested Python package | `src/dstoolkit/`, `tests/` | Metrics, bootstrap CIs, a custom scikit-learn transformer, SQL helpers, a colour-blind-safe plotting style, multiple-testing corrections; 29 unit tests with hand-calculated expected values |
| SQL analytics script | `sql/patient_analytics.sql` | 8 named queries: joins, CTE, window functions, subquery, aggregation (cross-checked against Pandas) |
| ML pipeline + model card | `models/` | Leak-free pipeline, tuned Ridge, `joblib` file and `model_card.json` |
| Chart gallery | `outputs/figures/` | 14 PNG charts and 1 SVG |
| Reproducible environment | `requirements.txt`, `requirements-lock.txt` | Pinned versions from the executed run |
| Documented notebook | `notebooks/Data_Science_Tool_Mastery.ipynb` | 10 sections, each exercise with code, output and observation |

## Tools demonstrated

| Tool | Highlights |
|---|---|
| Git | Live workflow in a temporary repo: commits, branches, `.gitignore`, a merge conflict resolved, history graph |
| NumPy | Broadcasting, `einsum`, regression from scratch (normal equations, gradient descent), bootstrap, floating-point pitfall found and fixed |
| Pandas | Method chaining, groupby (agg/transform/filter), time series, reshaping, validated merges, memory optimisation |
| SQL | CTEs, window functions, subqueries, indexes and query plans, transactions, parameterised queries |
| Matplotlib / Seaborn | Dashboards, statistical plots, clustermap, PNG and SVG export |
| Scikit-learn | Pipelines, leakage demonstration, feature ablation, model comparison, tuning, nested CV, interpretation, persistence |
| SciPy | Hypothesis tests, effect sizes, multiple-testing correction, regression inference built by hand |
| unittest | Known-value tests, edge cases, a mutation check, docstring audit |

**Not demonstrated** (not available in the build environment, listed as next steps in the notebook): Plotly, statsmodels, pytest, XGBoost / LightGBM, SHAP, Ruff / Black, DuckDB / Polars.

## Data

- **Real:** the *Diabetes* dataset (442 patients, 10 baseline variables, disease progression after one year): Efron, Hastie, Johnstone and Tibshirani (2004), *Least Angle Regression*, Annals of Statistics 32(2). A copy ships with scikit-learn; `src/prepare_dataset.py` exports it in original units to `data/raw/diabetes_raw.csv`.
- **Synthetic, clearly labelled, used in two places only:** simulated daily clinic visits (time-series exercise) and pure-noise data (data-leakage demonstration).

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
jupyter notebook                # open notebooks/Data_Science_Tool_Mastery.ipynb  (Kernel -> Restart & Run All)

# run the automated tests (from the project root)
PYTHONPATH=src python -m unittest discover -s tests -v          # Windows PowerShell: $env:PYTHONPATH="src"
```

The notebook needs `git` installed for the Git exercise.

## Key results

- On pure noise, a **leaky** workflow reports a cross-validated R² of about +0.2, while the correct pipeline reports about -0.6 (the truth).
- A **feature ablation** on training data showed that two engineered features added nothing measurable (RMSE spread 0.15 vs fold noise of about 3.5), and one of them made predictions drop by about 14 points whenever BMI crossed 25 or 30. It was dropped.
- Final model (tuned Ridge): test RMSE about 54 vs 73 for the baseline, R² about 0.45, with a wide bootstrap interval because the test set has only 89 patients.
- The hand-built regression, the bootstrap and scikit-learn agree (BMI 95% intervals [18.5, 30.9] analytic and [18.3, 31.1] bootstrap).

## Environment used

Python 3.12; exact versions in `requirements-lock.txt`. Other recent versions are expected to work but only these were tested. With Pandas 2.x text columns show as `object` instead of `str`.

## Limitations

Small, single-study dataset; the model explains under half of the variation; interpretation is associational, not causal. See Section 10 of the notebook for an honest self-assessment.

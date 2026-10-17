# Hands-On Data Lab Implementation

A complete, reproducible data-analysis lab built with **Python, Jupyter Notebook, NumPy, Pandas, Matplotlib, Seaborn and Scikit-learn**.
The notebook walks through environment setup, NumPy and Pandas practice, data cleaning, visualization and basic analysis, and documents the code, output and observation for every exercise.

> **About the data:** the datasets are **synthetic**. They were generated with a fixed random seed (`src/generate_data.py`) and contain deliberately injected data-quality problems (duplicates, missing values, inconsistent text, wrong data types, impossible values) so that the cleaning exercises are realistic. Patterns in the data illustrate the techniques; they are not real-world findings.

## Lab objectives and where they are covered

| # | Objective | Notebook section |
|---|---|---|
| 1 | Set up the Data Science environment | 1 |
| 2 | Work with data using Pandas & NumPy | 2, 3, 5 |
| 3 | Perform data cleaning | 4 |
| 4 | Create data visualizations | 6 (12 charts) |
| 5 | Perform basic data analysis | 7 |
| 6 | Complete & document practical exercises | All sections; summary in 8-9 |

## Project structure

```
hands-on-data-lab/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  orders.csv, customers.csv, products.csv   (messy input, never modified)
│   └── processed/            orders_clean.csv, customers_clean.csv     (output of the cleaning section)
├── notebooks/
│   └── Hands_On_Data_Lab.ipynb   main deliverable (code + outputs + charts + observations)
├── src/
│   └── generate_data.py      recreates the raw datasets (seed = 42)
└── outputs/
    └── figures/              12 saved charts (PNG)
```

## How to run

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 2. Install the libraries
pip install -r requirements.txt

# 3. Start Jupyter and open notebooks/Hands_On_Data_Lab.ipynb
jupyter notebook
```

In Jupyter choose **Kernel -> Restart & Run All** to reproduce every output and chart.
The raw CSV files are included, so `generate_data.py` does **not** need to be run. If you do regenerate the data (`python src/generate_data.py`), results can differ slightly with other NumPy versions.

## What the notebook covers

- **Environment:** installation steps, version check, imports, seeded random generator, relative paths.
- **NumPy:** array creation, vectorization and broadcasting, speed comparison with Python loops, indexing and masks, statistics, z-score and min-max scaling.
- **Pandas fundamentals:** loading, inspection, selection (`loc`, `iloc`), filtering, sorting.
- **Data cleaning:** quality audit, duplicates, inconsistent text, data types, invalid values and outliers, missing values (four strategies), validation with `assert`, saving clean data.
- **Merging, transformation, aggregation:** left joins with validation, new columns, binning, `groupby`, pivot tables, cross-tabs, rolling and cumulative values.
- **Visualization (12 charts):** bar, count plot, line, histograms, scatter with trend line, bar with confidence intervals, box plots, correlation heat map, pivot heat map, stacked bar.
- **Analysis:** descriptive statistics, distributions, Pearson and Spearman correlation, pattern checks, and a first Scikit-learn model (train/test split, baseline comparison, scaling).

## Environment used

The notebook was executed with Python 3.12, NumPy 2.4, Pandas 3.0, Matplotlib 3.10, Seaborn 0.13, Scikit-learn 1.8 and SciPy 1.17. Other recent versions are expected to work, but only these were tested. (With Pandas 2.x, text columns are shown as `object` instead of `str`.)

## Limitations

The data is synthetic, the sample is small (about 500 orders), and some cleaning decisions rely on stated assumptions (for example, a missing discount is treated as 0%). See Section 8 of the notebook.

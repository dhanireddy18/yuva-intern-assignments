# Real-World Dataset Analysis Project

**What distinguishes malignant from benign breast tumours?** An end-to-end exploratory analysis of the *Breast Cancer Wisconsin (Diagnostic)* dataset using Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy and Scikit-learn.

> Educational project. Nothing here is medical advice, and the model is **not** a diagnostic tool.

## The dataset (real-world data)

| Item | Detail |
|---|---|
| Name | Breast Cancer Wisconsin (Diagnostic), "WDBC" |
| Source | UCI Machine Learning Repository |
| Creators | Dr. William H. Wolberg, W. Nick Street, Olvi L. Mangasarian (University of Wisconsin); donated 1995 |
| Reference | Street, Wolberg & Mangasarian (1993), *Nuclear feature extraction for breast tumor diagnosis*, IS&T/SPIE Int. Symposium on Electronic Imaging, vol. 1905, pp. 861-870 |
| Content | 569 patients, 30 numeric measurements of cell nuclei (from digitized fine-needle-aspirate images), diagnosis = malignant (212) or benign (357) |
| How obtained here | An unmodified copy ships with scikit-learn (`load_breast_cancer`); `src/prepare_dataset.py` exports it **without any cleaning** to `data/raw/wdbc_raw.csv` |

The dataset is a curated research file: it has no missing values and no duplicates. The notebook reports this honestly and concentrates on the checks and decisions that matter (target recoding, meaningful zeros, outliers that carry real signal, skewness, redundancy, scaling).

## Project objectives and where they are covered

| # | Objective | Notebook section |
|---|---|---|
| 1 | Select a real-world dataset and understand its context | 1 |
| 2 | Explore the dataset | 2 |
| 3 | Clean and preprocess the data | 3 |
| 4 | Perform exploratory data analysis | 4 |
| 5 | Create data visualizations (15 charts) | 5 |
| 6 | Present insights and interpretations | 6 |

## Project structure

```
real-world-dataset-analysis/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/wdbc_raw.csv              unmodified dataset (never changed by the notebook)
│   └── processed/                    wdbc_clean.csv, reduced_features.csv
├── notebooks/
│   └── Real_World_Dataset_Analysis.ipynb   main deliverable
├── src/
│   └── prepare_dataset.py            exports the raw dataset from scikit-learn
└── outputs/figures/                  15 saved charts (PNG)
```

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
jupyter notebook                # open notebooks/Real_World_Dataset_Analysis.ipynb
```

In Jupyter choose **Kernel -> Restart & Run All** to reproduce every output and chart. The raw CSV is included, so `prepare_dataset.py` only needs to be run if you want to recreate it.

## Main findings

- Malignant tumours have larger and more irregular nuclei: the best features differ by more than **2.6 standard deviations** (Cohen's d), and 20 of the 30 features show a large effect.
- The share of malignant cases rises from **0% to 100%** across ten bands of `worst_perimeter`; the diagnosis is genuinely mixed only for about 20% of patients.
- The 30 measurements are highly redundant (21 pairs with |r| > 0.90): 21 low-redundancy features or 7 principal components carry almost all the information.
- Outliers in the size features are almost all malignant tumours (real signal), so they were **kept**.
- A simple logistic regression reaches about **97% cross-validated accuracy and 94% recall** for malignant cases. These are optimistic numbers from a curated research dataset.

## Environment used

Python 3.12, NumPy 2.4, Pandas 3.0, Matplotlib 3.10, Seaborn 0.13, SciPy 1.17, Scikit-learn 1.8. Other recent versions are expected to work but only these were tested. (With Pandas 2.x, text columns show as `object` instead of `str`.)

## Limitations

Single-source, curated data from the 1990s; pre-computed features rather than images; no patient context; association is not causation; model performance is optimistic and not clinically validated. See Section 6.4 of the notebook.

"""Export the real-world dataset used in this project to CSV.

Dataset : Breast Cancer Wisconsin (Diagnostic) - UCI Machine Learning Repository
Creators: Dr. William H. Wolberg, W. Nick Street, Olvi L. Mangasarian (University of Wisconsin); donated 1995
Access  : scikit-learn ships an unmodified copy of the UCI file (sklearn.datasets.load_breast_cancer).
          It is exported here WITHOUT any cleaning, so data/raw/wdbc_raw.csv is the raw starting point
          (column names contain spaces; target coded 0 = malignant, 1 = benign, exactly as distributed).

Run from the project root:  python src/prepare_dataset.py
"""
from pathlib import Path

from sklearn.datasets import load_breast_cancer

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
frame = load_breast_cancer(as_frame=True).frame
frame.to_csv(RAW / "wdbc_raw.csv", index=False)
print("saved", RAW / "wdbc_raw.csv", frame.shape)

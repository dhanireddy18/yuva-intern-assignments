"""Export the real-world dataset used in this project to CSV (raw, unscaled values).

Dataset : Diabetes dataset - 442 diabetes patients, ten baseline variables and a quantitative
          measure of disease progression one year after baseline.
Source  : Bradley Efron, Trevor Hastie, Iain Johnstone and Robert Tibshirani (2004),
          "Least Angle Regression", Annals of Statistics 32(2), 407-499.
Access  : scikit-learn ships a copy (sklearn.datasets.load_diabetes). ``scaled=False`` returns the
          values in their original units (age in years, BMI, blood pressure, serum measurements).

Run from the project root:  python src/prepare_dataset.py
"""
from pathlib import Path

from sklearn.datasets import load_diabetes

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
frame = load_diabetes(as_frame=True, scaled=False).frame
frame.to_csv(RAW / "diabetes_raw.csv", index=False)
print("saved", RAW / "diabetes_raw.csv", frame.shape)

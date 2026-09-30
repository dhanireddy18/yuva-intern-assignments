from pathlib import Path
import pandas as pd
import numpy as np

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "student_performance.csv"

def main():
    df = pd.read_csv(DATA_PATH)
    marks = df["Marks"]

    print("=== Descriptive Statistics ===")
    print(f"Mean: {marks.mean():.2f}")
    print(f"Median: {marks.median():.2f}")
    print(f"Mode: {marks.mode().tolist()}")
    print(f"Variance: {marks.var(ddof=0):.2f}")
    print(f"Standard deviation: {marks.std(ddof=0):.2f}")
    print(f"25th percentile: {np.percentile(marks, 25):.2f}")
    print(f"50th percentile: {np.percentile(marks, 50):.2f}")
    print(f"75th percentile: {np.percentile(marks, 75):.2f}")
    print(f"Correlation (study hours, marks): {df['Study_Hours'].corr(df['Marks']):.3f}")

if __name__ == "__main__":
    main()

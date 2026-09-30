from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "student_performance.csv"

def classify_marks(mark):
    if mark >= 75:
        return "High"
    if mark >= 60:
        return "Medium"
    return "Low"

def main():
    df = pd.read_csv(DATA_PATH)

    print("=== Dataset Preview ===")
    print(df.head())
    print("\n=== Data Types ===")
    print(df.dtypes)
    print("\n=== Missing Values ===")
    print(df.isnull().sum())
    print("\n=== Duplicate Rows ===")
    print(df.duplicated().sum())
    print("\n=== Summary ===")
    print(df.describe())

    df["Performance_Level"] = df["Marks"].apply(classify_marks)

    print("\n=== High Performers ===")
    print(df[df["Marks"] >= 75][["Student", "Marks", "Performance_Level"]])

    print("\n=== Sorted by Marks ===")
    print(df.sort_values("Marks", ascending=False)[["Student", "Marks"]])

    print("\n=== Average Marks by Performance Level ===")
    print(df.groupby("Performance_Level")["Marks"].mean())

if __name__ == "__main__":
    main()

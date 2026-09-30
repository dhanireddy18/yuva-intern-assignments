from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "student_performance.csv"
OUT = BASE / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH)

    plt.figure(figsize=(8, 5))
    plt.scatter(df["Study_Hours"], df["Marks"])
    plt.xlabel("Study Hours")
    plt.ylabel("Marks")
    plt.title("Study Hours vs Marks")
    plt.tight_layout()
    plt.savefig(OUT / "study_hours_vs_marks.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(df["Marks"], bins=5)
    plt.xlabel("Marks")
    plt.ylabel("Number of Students")
    plt.title("Distribution of Marks")
    plt.tight_layout()
    plt.savefig(OUT / "marks_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(df["Student"], df["Marks"])
    plt.xlabel("Student")
    plt.ylabel("Marks")
    plt.title("Student Marks")
    plt.tight_layout()
    plt.savefig(OUT / "student_marks.png", dpi=150)
    plt.close()

    print(f"Charts saved to: {OUT}")

if __name__ == "__main__":
    main()

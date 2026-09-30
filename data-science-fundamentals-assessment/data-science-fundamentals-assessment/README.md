# Data Science Fundamentals Assessment

This project is a practical implementation of the **Data Science Fundamentals Assessment**.

## Objectives
- Understand the Data Science lifecycle and types of analysis.
- Practice Python programming fundamentals.
- Apply descriptive statistics and probability concepts.
- Work with numerical, categorical, ordinal, datetime and text data.
- Perform data cleaning, exploration, filtering, sorting, grouping and correlation analysis.
- Create visualizations using Matplotlib.
- Follow clean, reproducible and responsible Data Science practices.

## Project Structure
```text
data-science-fundamentals-assessment/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── student_performance.csv
├── notebooks/
│   └── Data_Science_Fundamentals_Assessment.ipynb
├── src/
│   ├── __init__.py
│   ├── statistics_analysis.py
│   ├── data_analysis.py
│   └── visualization.py
├── reports/
│   └── Data_Science_Fundamentals_Assessment_Report.docx
└── outputs/
    └── charts/
```

## Dataset
The sample dataset contains 10 students and these fields:
- `Student`
- `Study_Hours`
- `Attendance`
- `Assignments`
- `Marks`

## Setup
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run the Notebook
```bash
jupyter notebook
```
Open `notebooks/Data_Science_Fundamentals_Assessment.ipynb`.

## Run Python Scripts
From the project root:
```bash
python src/statistics_analysis.py
python src/data_analysis.py
python src/visualization.py
```

## Main Findings
For the sample data:
- Average marks: **69.1**
- Highest marks: **90**
- Lowest marks: **50**
- Average attendance: **85.0%**
- Average study hours: **5.4**
- Student J has the highest marks in this sample.

These observations describe this small sample only and should not be treated as universal conclusions about student performance.

## GitHub Submission
Repository:
https://github.com/dhanireddy18/yuva-intern-assignments

Recommended folder:
`data-science-fundamentals-assessment/`

## Report
The `reports/` folder contains the Word report required for submission.

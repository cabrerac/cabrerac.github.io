---
course_code: 26-udenar-big-data
title: Diagnostic — Python and data skills
description: Ungraded baseline check before Lecture 1. Format F3 — guided code cells with light auto-checks plus short written answers. Dataset — UCI Adult (Census Income). Upload your completed .ipynb to Moodle as diagnostic_apellido_nombre.ipynb.
session: 0
start_time: 08:00 am
end_time: 12:00 pm
hours: 1.5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: diagnostic
lecture_date: 29/05/2026
permalink: /teaching/26-udenar-big-data/diagnostic/
visible: false
---

<!-- RENDER: -->

## Before you start

1. **This notebook is not graded.** It helps the instructor adapt the course and form balanced groups.
2. Open in **Google Colab** (link on this page) or download the `.ipynb` and run locally.
3. Work through every section in order. Read the instructions in each cell before running code.
4. When finished, **upload your completed notebook to Moodle** as `diagnostic_apellido_nombre.ipynb`.
5. Optional: return to the intake form (Section 5) and note how many exercises you completed.

**Estimated time:** 45–60 minutes.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Instructions (read first)

**Purpose.** This diagnostic is **not graded**. It measures your starting point in Python, pandas, SQL, and reading data — so we can support you in Lecture 1.

**How to work.**

1. Run cells **top to bottom** unless a cell tells you otherwise.
2. Cells marked **Your turn** expect you to write or fix code. Cells with **Check** run automatic tests — re-run until they pass.
3. Short-answer cells ask you to write **2–4 sentences** in your own words (Spanish or English).
4. At the end, run the **Submission** cell and follow the upload instructions.

**Dataset.** [UCI Adult / Census Income](https://archive.ics.uci.edu/dataset/2/adult) — a well-known public dataset about employment and income (similar themes to our course spine, but much smaller).

```python
# Setup — run once
import pandas as pd
import matplotlib.pyplot as plt

print("Environment OK")
```

## Band 1 — Python basics

**Your turn:** Create a variable `course` with value `"Big Data"` and print a greeting that includes it.

```python
# Your code here
course = "Big Data"
print(f"Hello, {course}!")
```

**Check:** Run the cell below after yours.

```python
assert course == "Big Data"
print("Band 1 — Python basics: OK")
```

## Band 2 — pandas — load and inspect

Download the Adult dataset (instructor-hosted CSV in the course bundle; fallback URL below).

```python
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country", "income",
]
df = pd.read_csv(URL, names=COLUMNS, skipinitialspace=True, na_values="?")
print(df.shape)
df.head()
```

**Your turn:** Print the number of rows and column names.

```python
n_rows = len(df)
columns = list(df.columns)
print(n_rows, columns[:3], "...")
```

**Check:**

```python
assert n_rows > 30000
assert "income" in df.columns
print("Band 2 — load and inspect: OK")
```

## Band 3 — pandas — filter and aggregate

**Your turn:** Count how many rows have `income == ">50K"`. Store the result in `high_income_count`.

```python
high_income_count = None  # replace with your code
```

**Check:**

```python
assert high_income_count is not None
assert high_income_count > 7000
print(f"High income count: {high_income_count}")
print("Band 3 — filter: OK")
```

## Band 4 — SQL with DuckDB

**Your turn:** Using DuckDB, compute the average `age` for rows where `sex == " Female"` (note leading space in raw data). Store in `avg_age_female`.

```python
import duckdb
avg_age_female = duckdb.sql("""
  SELECT AVG(age) FROM df WHERE sex = ' Female'
""").fetchone()[0]
print(avg_age_female)
```

**Check:**

```python
assert avg_age_female is not None
assert 35 < avg_age_female < 45
print("Band 4 — SQL: OK")
```

## Band 5 — Visualisation

**Your turn:** Plot a histogram of `age` with at least a title and x-label.

```python
plt.hist(df["age"], bins=20, edgecolor="black")
plt.title("Age distribution — Adult dataset")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()
```

## Band 6 — Reading data (short answer)

In **2–4 sentences** (Spanish or English): what does the histogram suggest about the age of people in this sample? Mention one limitation of histograms for this kind of data.

*(Write your answer in a new markdown cell below, or in the Moodle upload comment.)*

## Submission

Run this cell when all checks pass. Then upload the notebook to Moodle.

```python
passed = 0
checks = [
    ("Band 1", "course" in dir() and course == "Big Data"),
    ("Band 2", n_rows > 30000 if "n_rows" in dir() else False),
    ("Band 3", high_income_count is not None if "high_income_count" in dir() else False),
    ("Band 4", avg_age_female is not None if "avg_age_female" in dir() else False),
]
for name, ok in checks:
    if ok:
        passed += 1
    print(f"{name}: {'OK' if ok else 'incomplete'}")

print(f"\nDIAGNOSTIC_SCORE={passed}")
print("Upload this .ipynb to Moodle as diagnostic_apellido_nombre.ipynb")
```

<!-- end NOTEBOOK: -->

<!-- NOTEBOOK: -->

## Instructions (read first)

**Purpose.** This diagnostic is **not graded**. It measures your starting point in Python, pandas, and reading data, so we can form balanced groups and adapt support during the course.

**Honesty (required).** This exercise only works if you are honest:

- Do the **Your turn** cells yourself.
- Run the **Submission** cell and report the **real** `DIAGNOSTIC_SCORE` it prints (0–6) in the intake form. Do not inflate or lower your score.
- The instructor does **not** grade this notebook. We use your self-reported score together with the form to plan the course, not to assign a grade.

**What to do (in order).**

1. Open this notebook in **Google Colab** (use the link from your course email or the intake form).
2. Run cells **top to bottom** unless a cell tells you otherwise.
3. In cells marked **Your turn**, write the code yourself. In cells marked **Check**, run the tests and fix your code until the check passes.
4. Run the final **Submission** cell. It prints `DIAGNOSTIC_SCORE=n` (0–6).
5. Open the **intake form** [here](https://docs.google.com/forms/d/e/1FAIpQLSddAP60BHPP-DZ_a0pXrj8v96tPCuapWWR8tEJEzqgOvnr2QQ/viewform) and complete it. In **Section 5**, enter your score and how many bands you completed. You may **edit your form response** later if you finish more bands.

**Dataset.** [UCI Adult / Census Income](https://archive.ics.uci.edu/dataset/2/adult). A well-known public dataset (~32k rows) about employment and income.

## Setup

Run the following cells once. The loader tries the canonical UCI URL first, then a course-hosted copy, then a `scikit-learn` fallback. You should not get stuck on network issues.

We start with the required imports.

```python
import pandas as pd
import matplotlib.pyplot as plt
```

Let's define some relevant variables for our exercise

```python
COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country", "income",
]
UCI_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
COURSE_URL = "https://cabrerac.github.io/assets/data/26-udenar-big-data/adult.csv"
```

And now, let's create a function to download and access our dataset.

```python
def load_adult():
    # 1) UCI direct (canonical)
    try:
        df = pd.read_csv(UCI_URL, names=COLUMNS, skipinitialspace=True, na_values="?")
        print(f"Loaded {df.shape[0]:,} rows from UCI direct.")
        return df
    except Exception as e:
        print(f"UCI direct failed ({type(e).__name__}); trying course bundle...")
    # 2) Course-hosted bundle on the instructor website
    try:
        df = pd.read_csv(COURSE_URL)
        print(f"Loaded {df.shape[0]:,} rows from course bundle.")
        return df
    except Exception as e:
        print(f"Course bundle failed ({type(e).__name__}); trying sklearn fetch_openml...")
    # 3) sklearn fetch_openml (final fallback; needs scikit-learn)
    from sklearn.datasets import fetch_openml
    bunch = fetch_openml("adult", version=2, as_frame=True)
    df = bunch.frame.copy()
    df.columns = [c.replace(".", "-") for c in df.columns]
    if "class" in df.columns:
        df = df.rename(columns={"class": "income"})
    print(f"Loaded {df.shape[0]:,} rows from sklearn fetch_openml.")
    return df
df = load_adult()
print("Shape:", df.shape)
df.head()
```

## Band 1 - Python basics

**Your turn:** Create a variable `course` whose value is the string `"Big Data"`, then print a greeting that includes it (e.g. `"Hello, Big Data!"`).

```python
# YOUR CODE HERE
course = ...
# print(...)
```

**Check:**

```python
assert isinstance(course, str), "course must be a string"
assert course == "Big Data", "course must be exactly 'Big Data'"
print("Band 1 - Python basics: OK")
```

## Band 2 - pandas — inspect the dataset

**Your turn:** Store the **number of rows** of `df` in `n_rows` and the **list of column names** in `columns`. (Hint: `len(df)`, `list(df.columns)`.)

```python
# YOUR CODE HERE
n_rows = ...
columns = ...
print(n_rows, columns[:3], "...")
```

**Check:**

```python
assert isinstance(n_rows, int) and n_rows > 30000, "Expected ~32k rows"
assert isinstance(columns, list) and "income" in columns, "columns should include 'income'"
print("Band 2 - inspect: OK")
```

## Band 3 - pandas — filter and count

**Your turn:** Count how many rows have `income == ">50K"`. Store the result in `high_income_count` (an integer).

```python
# YOUR CODE HERE
high_income_count = ...
print(f"High income count: {high_income_count}")
```

**Check:**

```python
assert isinstance(high_income_count, int), "high_income_count must be an integer"
assert 7000 < high_income_count < 9000, "Expected ~7.8k rows with income > 50K"
print("Band 3 - filter: OK")
```

## Band 4 - pandas, groupby, and aggregate

**Your turn:** Compute the **mean** `hours-per-week` for each value of `sex`. Store the result in `mean_hours_by_sex` (a pandas Series indexed by `sex`). (Hint: `df.groupby(...)[...].mean()`.)

```python
# YOUR CODE HERE
mean_hours_by_sex = ...
print(mean_hours_by_sex)
```

**Check:**

```python
assert isinstance(mean_hours_by_sex, pd.Series), "mean_hours_by_sex must be a pandas Series (use df.groupby(...)[...].mean())"
assert "Male" in mean_hours_by_sex.index and "Female" in mean_hours_by_sex.index, "Series should be indexed by sex categories"
assert 40 < mean_hours_by_sex["Male"] < 45, "Male mean ~ 42.4 hours/week"
assert 33 < mean_hours_by_sex["Female"] < 40, "Female mean ~ 36.4 hours/week"
print("Band 4 - groupby: OK")
```

## Band 5 - Visualisation

**Your turn:** Produce a **histogram of `age`** on the axes provided. Add a **title** and an **x-axis label**.

```python
# YOUR CODE HERE — fill in the plotting commands
fig, ax = plt.subplots(figsize=(7, 4))
# ax.hist(...)
# ax.set_title(...)
# ax.set_xlabel(...)
# ax.set_ylabel(...)
plt.show()
```

**Check:**

```python
import matplotlib
assert isinstance(fig, matplotlib.figure.Figure), "Expected a matplotlib Figure named 'fig'"
assert len(ax.patches) > 0, "No histogram bars detected — did you call ax.hist(...)?"
assert ax.get_title().strip() != "", "Add a title with ax.set_title(...)"
assert ax.get_xlabel().strip() != "", "Add an x-label with ax.set_xlabel(...)"
print("Band 5 - visualisation: OK")
```

## Band 6 - Short answer

**Your turn:** In **2–4 sentences (Spanish or English)**, answer:

- What does the histogram from Band 5 suggest about the age distribution in this sample?
- State **one limitation** of using a histogram for this kind of data.

Replace the empty string in `b6_answer` with your answer.

```python
b6_answer = """

"""
print(b6_answer.strip()[:200])
```

**Check:**

```python
assert isinstance(b6_answer, str), "b6_answer must be a string"
assert len(b6_answer.strip()) >= 80, "Write at least ~2 sentences (≥ 80 characters)"
print("Band 6 - short answer: OK")
```

## Submission

Run this cell after all band checks have passed (or as far as you got). It prints your `DIAGNOSTIC_SCORE` (0–6). Copy that number into **Section 5** of the intake form.

[Intake form link](https://docs.google.com/forms/d/e/1FAIpQLSddAP60BHPP-DZ_a0pXrj8v96tPCuapWWR8tEJEzqgOvnr2QQ/viewform)

Report your score honestly — do not change the number to match what you wish you had scored.

```python
def _band_ok(name, predicate):
    try:
        return bool(predicate())
    except Exception:
        return False
checks = [
    ("Band 1 - Python basics", lambda: "course" in globals() and course == "Big Data"),
    ("Band 2 - inspect",       lambda: isinstance(n_rows, int) and n_rows > 30000 and "income" in columns),
    ("Band 3 - filter",        lambda: isinstance(high_income_count, int) and 7000 < high_income_count < 9000),
    ("Band 4 - groupby",       lambda: mean_hours_by_sex is not None and 40 < mean_hours_by_sex["Male"] < 45 and 33 < mean_hours_by_sex["Female"] < 40),
    ("Band 5 - visualisation", lambda: len(ax.patches) > 0 and ax.get_title().strip() != "" and ax.get_xlabel().strip() != ""),
    ("Band 6 - short answer",  lambda: isinstance(b6_answer, str) and len(b6_answer.strip()) >= 80),
]
passed = 0
for name, predicate in checks:
    ok = _band_ok(name, predicate)
    passed += int(ok)
    print(f"{name}: {'OK' if ok else 'incomplete'}")
print(f"\nDIAGNOSTIC_SCORE={passed}")
print("Report this score honestly in Section 5 of the intake form")
```

<!-- end NOTEBOOK: -->

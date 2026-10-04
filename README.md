# Student Performance Analysis

An end-to-end, reproducible Python and Pandas analysis of final Portuguese grades for secondary-school students. The project inspects data quality, creates useful score and attendance bands, explores relationships, runs a small set of statistical tests, and saves charts and result tables. Findings are associations, not causal claims.

## Educational problem and objectives

Schools need to understand how performance varies with learning context and student background so that support can be investigated thoughtfully. This analysis describes final grade `G3` in relation to prior period grades, reported weekly study-time band, absences, parental education, school support, demographics, and other available factors. It does not estimate causal effects or predict individual students.

## Dataset

- **Source:** [UCI Machine Learning Repository: Student Performance](https://archive.ics.uci.edu/dataset/320/student%2Bperformance), Portuguese course file (`student-por.csv`). The bundled copy is a mirror of this public UCI dataset; the source repository is authoritative.
- **Cohort:** 649 records from two Portuguese secondary schools, collected for the 2005–2006 school year according to the source paper.
- **Shape:** 649 rows × 33 fields; no student ID is supplied.
- **Target:** `G3`, final Portuguese course grade (0–20).
- **Key fields:** `G1`, `G2` (period grades), `studytime` (four ordinal weekly-hour bands), `absences`, `schoolsup` (extra educational support), `Medu`/`Fedu` (parental education), `sex`, `age`, `internet`, `activities`, and household/background fields.
- **Limitations:** Small, geographically and institutionally narrow cohort; observational and self-reported context; no actual attendance percentage, assignment/exam split, test-preparation field, family income, or student identifier. `G2` is close in time to `G3`, so its strong relationship is descriptive and unsuitable as an independent causal factor.

## Technologies

Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, and Jupyter.

## Workflow

Raw CSV → data understanding → cleaning and validation → derived bands → EDA → correlation and group tests → visualizations → quantified findings and limitations.

## Data cleaning and transformation

The loader detects the delimiter, standardizes headers and category whitespace/case, converts numeric fields, removes exact duplicate rows, and marks impossible age, grade, or negative-absence values missing. Missing values are not imputed; the bundled source has no missing values or exact duplicates, and all grade values are within 0–20. Derived fields are `performance_category` (Low 0–9, Average 10–13, Good 14–16, Excellent 17–20), `attendance_category` (0–4, 5–10, and 11+ absences), `studytime_label` using the UCI ordinal definitions, and `grade_change_g1_g3`.

## EDA and statistical analysis

The notebook and script cover score distributions and categories, reported study-time bands, absences, previous-period grades, school support, parental education, gender, numeric correlations, and IQR outlier flags. Pearson correlation is used for numeric score pairs. Kruskal–Wallis compares G3 across the four ordinal study-time groups; Welch's two-sample t-test compares G3 by extra school-support status. Tests are descriptive and observational; the support group difference may reflect who received support rather than an effect of support. No test-preparation variable exists in this dataset.

## Key findings

See [results/key_findings.md](results/key_findings.md) and the machine-readable values in `results/metrics.json`. Highlights from the bundled 649 rows: mean G3 is 11.91/20; 15.41% are in the 0–9 Low band; G2 and G3 have Pearson r=0.919; absences and G3 have r=−0.091; mean G3 increases from 10.84 in studytime band 1 to 13.23 in band 3, then is 13.06 in band 4. These are observed patterns, not proof of influence.

## Project structure

```text
student-performance-analysis/
├── data/raw/student-por.csv
├── data/processed/cleaned_student_por.csv
├── notebooks/student_performance_analysis.ipynb
├── src/analysis.py
├── visualizations/*.png
├── results/analysis_summary.csv, performance_categories.csv, attendance_summary.csv,
│           studytime_summary.csv, score_correlations.csv, metrics.json, key_findings.md
├── documentation/project_documentation.md
├── requirements.txt
└── README.md
```

## Setup and run

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python src/analysis.py
jupyter notebook notebooks/student_performance_analysis.ipynb
```

The included CSV makes the analysis immediately runnable. To refresh it, download `student-por.csv` from the UCI dataset page into `data/raw/`. Script outputs are written to `results/` and `visualizations/` using paths relative to the project.

## Future improvements

Replicate across the Mathematics cohort and report subject-specific differences; validate findings on newer and more representative school data; include confidence intervals and assumption diagnostics; investigate sensitivity to grade band boundaries and absence thresholds; collect direct measures of attendance, preparation, and assignment/exam components.

# Project documentation

## Objective and problem statement

Describe the distribution of Portuguese course outcomes and examine how final grade G3 varies alongside academic history, study-time category, absences, school support, parental education, and demographics. The analysis is intended as a reproducible descriptive analyst workflow and a basis for questions educators could investigate. Observational relationships are not causal estimates.

## Dataset and data dictionary

The project uses the Portuguese course file from the [UCI Student Performance dataset](https://archive.ics.uci.edu/dataset/320/student%2Bperformance), distributed as `data/raw/student-por.csv`. The documented collection covers two Portuguese secondary schools and the 2005–2006 school year. The file has 649 rows and 33 columns. The original records do not provide student IDs.

| Field(s) | Meaning |
|---|---|
| `school`, `sex`, `age`, `address`, `famsize`, `Pstatus` | School, sex, age, home location, family size, parent cohabitation |
| `Medu`, `Fedu` | Mother/father education on the documented ordinal 0–4 scale |
| `Mjob`, `Fjob`, `reason`, `guardian` | Parent jobs, school-choice reason, guardian |
| `traveltime`, `studytime`, `failures` | Ordered travel-time and weekly study-time bands; past class failures |
| `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `higher`, `internet`, `romantic` | Yes/no student and household context indicators |
| `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health` | Self-reported ordinal context measures |
| `absences` | Count of school absences (not an attendance percentage) |
| `G1`, `G2`, `G3` | First-period, second-period, and final subject grades, 0–20 |

There is no direct test-preparation, sleep, assignment performance, exam component, or family-income field. Those variables are not inferred or fabricated.

## Data quality and cleaning

`load_clean_data` uses Pandas delimiter inference to read either the semicolon-delimited official UCI file or comma-delimited mirror. It strips header whitespace, lowercases names and category strings, parses numeric fields, and drops exact duplicate records. Scores outside 0–20, ages outside a conservative 13–25 range, and negative absences are set missing rather than replaced. The supplied dataset contains no missing cells, exact duplicate rows, or out-of-range grades/negative absences. No imputation is performed. IQR outliers are flagged and retained because unusual valid students are not data errors by default.

## Transformations

`performance_category` uses Low 0–9, Average 10–13, Good 14–16, and Excellent 17–20. The thresholds are transparent descriptive bins, not official grading decisions. `attendance_category` uses 0–4, 5–10, and 11+ absences; these are pragmatic analytical bands and not formal attendance standards. `studytime_label` translates the source ordinal codes: under 2, 2–5, 5–10, and over 10 weekly hours. `grade_change_g1_g3` is final minus first-period grade. These derived values do not replace source fields.

## EDA methodology

The analysis uses Pandas counts, descriptive statistics, grouped summaries, and category proportions. Matplotlib/Seaborn charts examine final-grade distribution, score bands, study-time and attendance patterns, G2 versus G3, school-support groups, parental education, and numeric-variable correlations. Titles, axes, and category definitions are kept explicit. IQR rules flag potential outliers in G3, studytime, and absences; no outlier is automatically removed.

## Statistical analysis

- **Pearson correlation:** G2 versus G3 and numeric fields versus G3. This measures linear association and does not establish cause. G2 is temporally close to the target.
- **Kruskal–Wallis:** compares G3 distributions across four independent ordinal studytime groups; chosen as a rank-based multi-group comparison. A small p-value indicates evidence that not all group distributions are the same, not a monotonic dose effect.
- **Welch t-test:** compares average G3 for students recorded as receiving versus not receiving extra school educational support; unequal variance is allowed. This is not a test-preparation comparison and cannot establish the effect of support, since assignment to support may be selective.

P-values are reported with the statistics in `results/metrics.json`. Tests are exploratory; multiple comparisons and sampling design limit inference. No causal claims are made.

## Key questions and observed findings

See `results/key_findings.md` for the computed answer sheet. In the provided file, mean G3 is 11.91, median 12, range 0–19. Category proportions are 15.41% Low, 54.70% Average, 22.80% Good, and 7.09% Excellent. Mean G3 by study-time category is 10.84, 12.09, 13.23, and 13.06. Mean G3 for attendance bands is 12.06 for 0–4 absences, 11.84 for 5–10, and 10.65 for 11+. Pearson r(G2,G3)=0.919; r(absences,G3)=−0.091. Extra school-support group means are 11.28 (yes) and 11.98 (no), a descriptive contrast likely affected by selection into support. Mother education group means range from 10.80 (level 1) to 13.07 (level 4), with small groups at lower levels.

The strongest raw numeric associations are G2 and G1, which are prior grades on the same course trajectory and thus partly encode existing performance. Excluding period grades, failures (r=−0.393) and studytime (r=0.250) have the largest absolute associations in the metrics output. Treat small coefficients cautiously.

## Educational interpretation

The descriptive patterns can motivate follow-up questions: whether students with more absences need additional engagement support; what resources students in lower study-time groups need; and whether school-support allocation reaches students who need it. The lower average among students receiving extra school support should not be interpreted as evidence that support harms scores: students may receive support because they are already struggling. These data do not measure intervention timing, dosage, or counterfactual outcomes.

## Assumptions and limitations

- The mirror is treated as an exact copy of UCI's Portuguese subset; `data/raw/README.md` records provenance and validation details.
- The dataset is historical, observational, and limited to two schools in Portugal; it is not representative of all students.
- Context is self-reported and measures are coarse ordinal categories.
- Missingness and duplicate handling findings refer to this distributed file.
- Grade bands and absence bands are analysis choices.
- Correlation and group comparisons do not prove causation; tests do not adjust for confounding or multiple comparisons.
- G1/G2 are close to G3, making their high correlations unsurprising and potentially unsuitable for prospective intervention claims.

## Reproducibility

Install `requirements.txt`, run `python src/analysis.py`, and open `notebooks/student_performance_analysis.ipynb` with Jupyter. All paths are project-relative. The script regenerates charts and results; the CSV is bundled under `data/raw/`.

## Future improvements

Compare Mathematics and Portuguese without double-counting the same student across cohorts; obtain newer multi-school data; report uncertainty intervals and diagnostics; validate whether findings persist under alternate group thresholds; and collect direct measurements of attendance, sleep, assessment components, and test preparation.

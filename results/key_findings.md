# Key findings

## Dataset summary

- 649 Portuguese-course student records and 33 source fields; target is final grade G3 on a 0–20 scale.
- Source file has 0 missing cells and 0 exact duplicate rows. No score outside 0–20 or negative absences were found; missing values are not imputed.
- Study time, absences, prior grades, support status, parental education, demographics, and household/lifestyle measures are available. There is no test-preparation variable.

## Overall performance

- Mean G3: **11.91**, median **12**, standard deviation **3.23**, range **0–19**.
- Bands: Low 0–9 **100 (15.41%)**; Average 10–13 **355 (54.70%)**; Good 14–16 **148 (22.80%)**; Excellent 17–20 **46 (7.09%)**.

## Relationships and statistical comparisons

- **Prior period grade:** G2 and G3 Pearson r = **0.919** (p = 5.64e-263); G1 and G3 r = **0.826**. These within-course grades are temporally close to G3.
- **Study time:** mean G3 by source band is 1.0: 10.84, 2.0: 12.09, 3.0: 13.23, 4.0: 13.06. The pattern increases through band 3 and is slightly lower in band 4; it is not strictly monotonic. Kruskal–Wallis H = 50.32, p = 6.84e-11.
- **Absences:** Pearson r with G3 = **-0.091**. Mean G3 is Higher attendance (0–4 absences): 12.06, Moderate (5–10): 11.84, Lower attendance (11+): 10.65 across 0–4, 5–10, and 11+ absence bands. The linear correlation is weak; the lower mean in the highest-absence band is descriptive.
- **Strongest numeric associations excluding G1/G2:** failures (r = -0.393); next studytime (r = 0.250). Small correlations are not strong evidence of practical importance.
- **School support:** students marked yes averaged 11.28; those marked no averaged 11.98. Welch t = -2.25, p = 0.0268. Support is likely targeted, so this difference does not estimate its effect. This dataset does not have test preparation.
- **Mother's education:** mean G3 across the documented 0–4 education levels: 0.0: 11.67, 1.0: 10.80, 2.0: 11.66, 3.0: 11.92, 4.0: 13.07. Group sizes differ, and low-level groups are small; interpret cautiously.
- **Gender:** mean G3 is f: 12.25, m: 11.41; this is a sample description, not a generalization.

## Outlier review

IQR flags: G3 **16**, ordinal studytime **35**, absences **21**. These records are retained; the rule flags statistical extremes, not data errors.

## Possible educational implications

The study-time and absence patterns can motivate follow-up on engagement and study support, but are not evidence that changing either factor alone will raise grades. The lower average among students receiving school support may reflect need-based assignment. Use these observations to ask better questions and evaluate supports with longitudinal or intervention data.

## Limitations

The cohort covers two Portuguese schools in 2005–2006 and is observational. Self-reported categorical context, unmeasured confounding, modest group sizes, arbitrary descriptive bands, and multiple exploratory comparisons limit inference. Correlation does not imply causation. G2/G1 are closely related to G3. No assignment/exam split, attendance percentage, sleep, income, or test-preparation measure exists.

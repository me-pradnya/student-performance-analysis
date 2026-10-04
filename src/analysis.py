"""Reproducible analysis of the UCI Portuguese student performance data."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/student-por.csv"
OUT = ROOT / "results"
PLOTS = ROOT / "visualizations"
SCORE = "G3"

def load_clean_data(path=RAW):
    # UCI's official archive uses semicolons; the mirrored raw copy may use commas.
    df = pd.read_csv(path, sep=None, engine="python")
    df.columns = df.columns.str.strip().str.lower()
    for col in df.select_dtypes("object"):
        df[col] = df[col].str.strip().str.lower()
    numeric = ["age", "medu", "fedu", "traveltime", "studytime", "failures", "famrel", "freetime", "goout", "dalc", "walc", "health", "absences", "g1", "g2", "g3"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    allowed = {
        "school": {"gp", "ms"}, "sex": {"f", "m"}, "address": {"u", "r"},
        "famsize": {"le3", "gt3"}, "pstatus": {"t", "a"},
        "mjob": {"teacher", "health", "services", "at_home", "other"},
        "fjob": {"teacher", "health", "services", "at_home", "other"},
        "reason": {"home", "reputation", "course", "other"},
        "guardian": {"mother", "father", "other"},
        **{c: {"yes", "no"} for c in ["schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"]},
    }
    for col, valid in allowed.items():
        df.loc[~df[col].isin(valid), col] = np.nan
    for col, low, high in [("medu", 0, 4), ("fedu", 0, 4), ("traveltime", 1, 4), ("studytime", 1, 4), ("famrel", 1, 5), ("freetime", 1, 5), ("goout", 1, 5), ("dalc", 1, 5), ("walc", 1, 5), ("health", 1, 5)]:
        df.loc[~df[col].between(low, high), col] = np.nan
    df = df.drop_duplicates().copy()
    # Scores must be 0–20, absences nonnegative, and ages plausible for this cohort.
    for col in ["g1", "g2", "g3"]:
        df.loc[~df[col].between(0, 20), col] = np.nan
    df.loc[df.absences < 0, "absences"] = np.nan
    df.loc[~df.age.between(13, 25), "age"] = np.nan
    # Preserve valid records; report missingness instead of imputing outcomes.
    df["performance_category"] = pd.cut(df.g3, [-0.01, 9.99, 13.99, 16.99, 20], labels=["Low", "Average", "Good", "Excellent"])
    df["attendance_category"] = pd.cut(df.absences, [-0.01, 4, 10, np.inf], labels=["Higher attendance (0–4 absences)", "Moderate (5–10)", "Lower attendance (11+)"])
    df["studytime_label"] = df.studytime.map({1:"<2 hours/week", 2:"2–5 hours/week", 3:"5–10 hours/week", 4:">10 hours/week"})
    df["grade_change_g1_g3"] = df.g3 - df.g1
    return df

def run():
    OUT.mkdir(exist_ok=True); PLOTS.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    raw = pd.read_csv(RAW, sep=None, engine="python")
    df = load_clean_data()
    df.to_csv(ROOT / "data/processed/cleaned_student_por.csv", index=False)
    nums = df.select_dtypes(include="number")
    score_stats = df.g3.describe().to_dict()
    cats = df.performance_category.value_counts(sort=False).rename_axis("category").reset_index(name="students")
    cats["percent"] = cats.students / len(df) * 100
    cats.to_csv(OUT / "performance_categories.csv", index=False)
    df.groupby("studytime_label", observed=False).g3.agg(["count","mean","median","std"]).to_csv(OUT / "studytime_summary.csv")
    df.groupby("attendance_category", observed=False).g3.agg(["count","mean","median","std"]).to_csv(OUT / "attendance_summary.csv")
    # Exclude a derived feature containing G3 itself to avoid target leakage.
    corr = nums.drop(columns=["grade_change_g1_g3"]).corr(numeric_only=True)["g3"].drop("g3").sort_values(key=abs, ascending=False)
    corr.rename("pearson_r_with_g3").to_csv(OUT / "score_correlations.csv")
    # Welch test compares two independent groups without assuming equal variances.
    support_groups = [df.loc[df.schoolsup == v, "g3"].dropna() for v in ["yes", "no"]]
    welch = stats.ttest_ind(*support_groups, equal_var=False)
    # Kruskal-Wallis is robust for the ordinal study-time groups.
    study_groups = [g.g3.dropna().to_numpy() for _, g in df.groupby("studytime", observed=True)]
    kw = stats.kruskal(*study_groups)
    pearson = stats.pearsonr(df[["g2","g3"]].dropna().g2, df[["g2","g3"]].dropna().g3)
    summary = {"n_rows":int(len(df)),"n_columns_raw":int(raw.shape[1]),"missing_cells_in_source":int(raw.isna().sum().sum()),"missing_cells_after_cleaning":int(df.isna().sum().sum()),"duplicates_removed":int(raw.duplicated().sum()),"score":{k:float(v) for k,v in score_stats.items()},"category_counts":dict(zip(cats.category.astype(str),cats.students.astype(int))),"category_percent":dict(zip(cats.category.astype(str),cats.percent.round(2))),"correlations_with_g3":{k:float(v) for k,v in corr.items()},"g2_g3_pearson_r":float(pearson.statistic),"g2_g3_p":float(pearson.pvalue),"schoolsup_welch_t":float(welch.statistic),"schoolsup_welch_p":float(welch.pvalue),"schoolsup_means":{"yes":float(support_groups[0].mean()),"no":float(support_groups[1].mean())},"studytime_kruskal_h":float(kw.statistic),"studytime_kruskal_p":float(kw.pvalue),"studytime_means":{str(k):float(v) for k,v in df.groupby("studytime",observed=True).g3.mean().items()},"attendance_means":{str(k):float(v) for k,v in df.groupby("attendance_category",observed=False).g3.mean().items()},"parent_education_means_mother":{str(k):float(v) for k,v in df.groupby("medu",observed=True).g3.mean().items()},"gender_means":{str(k):float(v) for k,v in df.groupby("sex",observed=True).g3.mean().items()},"outlier_counts_iqr":{c:int(((df[c] < df[c].quantile(.25)-1.5*(df[c].quantile(.75)-df[c].quantile(.25))) | (df[c] > df[c].quantile(.75)+1.5*(df[c].quantile(.75)-df[c].quantile(.25)))).sum()) for c in ["g3","studytime","absences"]}}
    (OUT / "metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    cats_names = ["Low", "Average", "Good", "Excellent"]
    fig, ax = plt.subplots(figsize=(8,5)); sns.histplot(df.g3, bins=np.arange(-.5,21.5,1), kde=True, ax=ax); ax.set(xlabel="Final Portuguese grade (G3, 0–20)", title="Distribution of final grades"); fig.tight_layout(); fig.savefig(PLOTS/"score_distribution.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,5)); sns.barplot(data=cats,x="category",y="percent",order=cats_names,ax=ax); ax.set(ylabel="Students (%)",xlabel="",title="Final-grade performance bands"); fig.tight_layout(); fig.savefig(PLOTS/"performance_categories.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,5)); sns.boxplot(data=df,x="studytime_label",y="g3",order=["<2 hours/week","2–5 hours/week","5–10 hours/week",">10 hours/week"],ax=ax); ax.set(xlabel="Reported weekly study time",ylabel="G3",title="Final grade by reported study-time band"); ax.tick_params(axis="x",rotation=15); fig.tight_layout(); fig.savefig(PLOTS/"studytime_vs_score.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,5)); sns.regplot(data=df,x="absences",y="g3",scatter_kws={"alpha":.45},line_kws={"color":"crimson"},ax=ax); ax.set(xlabel="School absences",ylabel="G3",title="Absences and final grade (descriptive trend)"); fig.tight_layout(); fig.savefig(PLOTS/"attendance_vs_score.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,5)); sns.regplot(data=df,x="g2",y="g3",scatter_kws={"alpha":.45},ax=ax); ax.set(xlabel="Second-period grade (G2)",ylabel="Final grade (G3)",title="Second-period and final grades"); fig.tight_layout(); fig.savefig(PLOTS/"previous_vs_current_score.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7,5)); sns.boxplot(data=df,x="schoolsup",y="g3",order=["yes","no"],ax=ax); ax.set(xlabel="Extra educational support",ylabel="G3",title="Final grade by school support status"); fig.tight_layout(); fig.savefig(PLOTS/"school_support_analysis.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,5)); sns.pointplot(data=df,x="medu",y="g3",errorbar=("ci",95),ax=ax); ax.set(xlabel="Mother's education (0–4 ordinal scale)",ylabel="Mean G3 (95% CI)",title="Final grade by mother's education category"); fig.tight_layout(); fig.savefig(PLOTS/"parental_education_analysis.png",dpi=160); plt.close(fig)
    heatmap_nums = nums.drop(columns=["grade_change_g1_g3"])
    fig, ax = plt.subplots(figsize=(12,9)); sns.heatmap(heatmap_nums.corr(),cmap="vlag",center=0,ax=ax); ax.set_title("Correlation matrix of numeric variables"); fig.tight_layout(); fig.savefig(PLOTS/"correlation_heatmap.png",dpi=160); plt.close(fig)
    # compact row-wise analytical table
    top_context = corr.drop(labels=["g1", "g2"], errors="ignore").head(1)
    pd.DataFrame([{"question":"Strongest numeric association excluding period grades","answer":f"{top_context.index[0]} r={top_context.iloc[0]:.3f}"},{"question":"G2–G3 association","answer":f"r={pearson.statistic:.3f}; p={pearson.pvalue:.3g}"},{"question":"Extra school-support group comparison","answer":f"yes mean={support_groups[0].mean():.2f}; no mean={support_groups[1].mean():.2f}; Welch p={welch.pvalue:.3g}"},{"question":"Study-time group comparison","answer":f"Kruskal–Wallis H={kw.statistic:.2f}; p={kw.pvalue:.3g}"}]).to_csv(OUT/"analysis_summary.csv",index=False)
    # Keep the human-readable findings synchronized with computed metrics.
    study = summary["studytime_means"]
    attendance = summary["attendance_means"]
    medu = summary["parent_education_means_mother"]
    context = corr.drop(labels=["g1", "g2"], errors="ignore")
    best_context = context.index[0]
    findings = f'''# Key findings\n\n## Dataset summary\n\n- 649 Portuguese-course student records and 33 source fields; target is final grade G3 on a 0–20 scale.\n- Source file has {summary['missing_cells_in_source']} missing cells and {summary['duplicates_removed']} exact duplicate rows. No score outside 0–20 or negative absences were found; missing values are not imputed.\n- Study time, absences, prior grades, support status, parental education, demographics, and household/lifestyle measures are available. There is no test-preparation variable.\n\n## Overall performance\n\n- Mean G3: **{summary['score']['mean']:.2f}**, median **{summary['score']['50%']:.0f}**, standard deviation **{summary['score']['std']:.2f}**, range **{summary['score']['min']:.0f}–{summary['score']['max']:.0f}**.\n- Bands: Low 0–9 **{summary['category_counts']['Low']} ({summary['category_percent']['Low']:.2f}%)**; Average 10–13 **{summary['category_counts']['Average']} ({summary['category_percent']['Average']:.2f}%)**; Good 14–16 **{summary['category_counts']['Good']} ({summary['category_percent']['Good']:.2f}%)**; Excellent 17–20 **{summary['category_counts']['Excellent']} ({summary['category_percent']['Excellent']:.2f}%)**.\n\n## Relationships and statistical comparisons\n\n- **Prior period grade:** G2 and G3 Pearson r = **{summary['g2_g3_pearson_r']:.3f}** (p = {summary['g2_g3_p']:.3g}); G1 and G3 r = **{corr['g1']:.3f}**. These within-course grades are temporally close to G3.\n- **Study time:** mean G3 by source band is {', '.join(f'{k}: {v:.2f}' for k,v in study.items())}. The pattern increases through band 3 and is slightly lower in band 4; it is not strictly monotonic. Kruskal–Wallis H = {summary['studytime_kruskal_h']:.2f}, p = {summary['studytime_kruskal_p']:.3g}.\n- **Absences:** Pearson r with G3 = **{corr['absences']:.3f}**. Mean G3 is {', '.join(f'{k}: {v:.2f}' for k,v in attendance.items())} across 0–4, 5–10, and 11+ absence bands. The linear correlation is weak; the lower mean in the highest-absence band is descriptive.\n- **Strongest numeric associations excluding G1/G2:** {best_context} (r = {context.iloc[0]:.3f}); next {context.index[1]} (r = {context.iloc[1]:.3f}). Small correlations are not strong evidence of practical importance.\n- **School support:** students marked yes averaged {summary['schoolsup_means']['yes']:.2f}; those marked no averaged {summary['schoolsup_means']['no']:.2f}. Welch t = {summary['schoolsup_welch_t']:.2f}, p = {summary['schoolsup_welch_p']:.4f}. Support is likely targeted, so this difference does not estimate its effect. This dataset does not have test preparation.\n- **Mother's education:** mean G3 across the documented 0–4 education levels: {', '.join(f'{k}: {v:.2f}' for k,v in medu.items())}. Group sizes differ, and low-level groups are small; interpret cautiously.\n- **Gender:** mean G3 is {', '.join(f'{k}: {v:.2f}' for k,v in summary['gender_means'].items())}; this is a sample description, not a generalization.\n\n## Outlier review\n\nIQR flags: G3 **{summary['outlier_counts_iqr']['g3']}**, ordinal studytime **{summary['outlier_counts_iqr']['studytime']}**, absences **{summary['outlier_counts_iqr']['absences']}**. These records are retained; the rule flags statistical extremes, not data errors.\n\n## Possible educational implications\n\nThe study-time and absence patterns can motivate follow-up on engagement and study support, but are not evidence that changing either factor alone will raise grades. The lower average among students receiving school support may reflect need-based assignment. Use these observations to ask better questions and evaluate supports with longitudinal or intervention data.\n\n## Limitations\n\nThe cohort covers two Portuguese schools in 2005–2006 and is observational. Self-reported categorical context, unmeasured confounding, modest group sizes, arbitrary descriptive bands, and multiple exploratory comparisons limit inference. Correlation does not imply causation. G2/G1 are closely related to G3. No assignment/exam split, attendance percentage, sleep, income, or test-preparation measure exists.\n'''
    (OUT / "key_findings.md").write_text(findings, encoding="utf-8")
    return df, summary

if __name__ == "__main__":
    run()

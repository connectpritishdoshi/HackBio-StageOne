# Exploring Genomics of Drug Sensitivity in Cancer (GDSC)
### HackBio Stage One — AI for Genomics Internship
### A Layman's Guide - Written for Curious Minds, Not Just Biologists

---

## Project Links

- **GitHub Repository:** https://github.com/connectpritishdoshi/HackBio-StageOne
- **LinkedIn:** https://www.linkedin.com/in/pritish-doshi-677141261/details/projects/

---

## The Problem We Are Solving

Imagine you are a doctor. You have 100 cancer patients sitting in front of you. Each one has a different type of cancer - lung, breast, bone, blood. You also have a shelf with 200 different drugs. Your goal sounds simple: **give the right drug to the right patient.**

But here is the hard truth - most cancer drugs do not work for everyone. A drug that shrinks a tumour in one patient might do absolutely nothing for the next. Worse, cancer drugs are often toxic. Giving the wrong one wastes precious time and causes unnecessary suffering.

So how do scientists figure out which drugs work on which cancers? They run thousands of laboratory experiments, collect the results, and then - this is where we come in - **analyse the data to find patterns.**

This project does exactly that, using a real-world dataset called **GDSC: Genomics of Drug Sensitivity in Cancer.**

---

## The Dataset: Our Giant Experiment Book

The GDSC dataset is a public scientific database. Scientists grew hundreds of different cancer cell lines in a lab - tiny living samples of real human cancers - and tested each one against hundreds of drugs. Every row in our dataset is one such experiment.

The **rows** are one drug tested on one cancer cell.
The **columns** describe everything about the test.

Here are the key columns and what they mean in plain English:

**Identifiers & Classifications**

*CELL_LINE_NAME* — The specific name of the cancer cell model being tested.

*TCGA_DESC* — The type of cancer (e.g., lung, colon, breast).

*DRUG_NAME* — The name of the pharmaceutical compound being tested against the cell line.

*TARGET_PATHWAY* — The specific biological mechanism or process the drug is designed to attack.

**Drug Response Metrics**

*LN_IC50* — How much drug was needed to kill 50% of the cancer cells. A lower value means the drug is more powerful (it took less of the drug to do the job).

*AUC* — Area Under the Curve. How well the drug worked across a full range of doses — a broader, overall measure of the drug's effectiveness.

*Z_SCORE* — A statistical measure showing how unusual or extreme this cell line's response is compared to the average of all other cell lines tested.

**Molecular & Genetic Features**

*CNA* — Copy Number Alteration. Indicates whether the cancer cell has a DNA copy error, such as a section of DNA being abnormally duplicated or deleted.

*Gene Expression* — Indicates whether a specific gene is unusually active (turned up) or silent (turned down) in this particular cancer.

*Methylation* — Indicates whether certain genes have been chemically "switched off" or muted by the cell.

> **The most important number — LN_IC50** is the heart of this dataset. A very low or very negative LN_IC50 means the drug is a precision weapon - a tiny amount is enough to kill the cancer cells. A high LN_IC50 means you would need a dangerously large dose to see any effect at all.

---

## Our Analysis: A 5-Step Investigation

Think of this project like a detective story. We start with a massive pile of raw data and, step by step, extract meaning from it.

---

### Step 1 — Understanding the Dataset
*What are we actually working with?*

Before drawing any conclusions, a good scientist gets to know their data intimately. We ask:

- **How many experiments are in the dataset?**
- **Are there gaps or errors?** We scan for missing values and duplicate entries.
- **Are the numbers actually stored as numbers?** We check and fix data types.
- **What does each column actually mean?** We cross-reference against a metadata file.

#### What We Found

Our dataset contains **162,103 experiments** across **19 columns** — every one of them complete, with no missing values and no duplicate rows. This is excellent data quality for a real-world biological dataset.

```
Total Rows:    162,103
Total Columns: 19
Missing Values: None
Duplicate Rows: 0
```

**Summary statistics for the key numeric columns:**

| Metric    | Mean   | Std Dev | Min     | Max    |
|-----------|--------|---------|---------|--------|
| LN_IC50   | 2.82   | 2.84    | -8.64   | 13.82  |
| AUC       | 0.88   | 0.15    | 0.006   | 0.999  |
| Z_SCORE   | 0.04   | 1.00    | -6.91   | 7.98   |

#### Biological Interpretation

The mean LN_IC50 of **2.82** tells us that on average, a moderate-to-high dose is required to inhibit cancer cell growth. But the wide standard deviation of **2.84** — nearly as large as the mean — is the critical signal here. It tells us drug effectiveness is **enormously variable** across cancer types. This is not noise; it is biology telling us that different cancers are fundamentally different diseases. A one-size-fits-all approach to cancer treatment is not just suboptimal — it is biologically inappropriate.

> **Why this matters biologically:** In real laboratory settings, data collection is messy. Machines malfunction, values get entered incorrectly, and experiments sometimes fail silently. Cleaning the data is not glamorous work, but skipping it is like building a house on sand. The fact that our dataset is clean and complete means every finding we report below can be trusted.

---

### Step 2 — Drug Sensitivity Patterns
*Which drugs are champions, and which are duds?*

We rank every single drug by how effective it is across all cancer cell lines tested.

#### Most Effective Drugs (Lowest Mean LN_IC50)

| Drug | Mean LN_IC50 | Std Dev |
|------|-------------|---------|
| Romidepsin | -5.178 | 1.027 |
| Bortezomib | -4.747 | 1.062 |
| Sepantronium bromide | -4.056 | 1.646 |
| Dactinomycin | -3.670 | 1.861 |
| SN-38 | -3.360 | 1.934 |
| Vinblastine | -3.354 | 2.199 |
| Docetaxel | -3.327 | 2.547 |
| Daporinab | -3.323 | 2.736 |
| Paclitaxel | -3.006 | 1.765 |
| Eg5_9814 | -2.887 | 1.784 |

#### Least Effective Drugs (Highest Mean LN_IC50)

| Drug | Mean LN_IC50 | Std Dev |
|------|-------------|---------|
| Ascorbate (Vitamin C) | 10.292 | 1.288 |
| N-acetyl cysteine | 9.988 | 0.871 |
| Glutathione | 9.181 | 0.904 |
| Alpha-lipoic acid | 7.672 | 1.002 |
| Temozolomide | 6.358 | 1.280 |

#### Drugs with Highly Variable Responses

| Drug | Mean LN_IC50 | Std Dev |
|------|-------------|---------|
| Gemcitabine | -0.632 | 2.942 |
| AZD5991 | 3.863 | 2.759 |
| Daporinab | -3.323 | 2.736 |
| Docetaxel | -3.327 | 2.547 |
| Dasatinib | 1.274 | 2.394 |

#### Biological Interpretation

**Romidepsin** stands out as the single most potent drug in the dataset, with a mean LN_IC50 of -5.18. It is a histone deacetylase (HDAC) inhibitor — a class of drugs that work by interfering with the proteins that control how tightly DNA is wound inside the cell. When these proteins are blocked, cancer cells lose the ability to silence their own self-destruct signals. The low standard deviation (1.03) means this effect is **consistent** — Romidepsin is broadly lethal to cancer regardless of cancer type.

**Bortezomib** (-4.75) is a proteasome inhibitor — it blocks the cell's internal "trash compactor" that normally breaks down damaged proteins. Without this, cancer cells drown in their own cellular waste and die. Again, the tight standard deviation confirms broad effectiveness.

In sharp contrast, **Vitamin C (ascorbate)**, **N-acetyl cysteine**, and **glutathione** are the least effective "drugs" tested — which is biologically expected. These are antioxidants, not targeted cancer killers. Their high LN_IC50 values simply confirm that nutritional supplements alone cannot directly kill cancer cells at practical doses.

**Dasatinib** and **Gemcitabine** are among the most variable — meaning they work brilliantly for some cancers and poorly for others. This is not a failure; it is a clue. It suggests these drugs are hitting a specific genetic target that only some cancers carry. Identifying *which* cancers respond to Dasatinib became one of the most important findings in our next step.

> **Biological insight:** A highly variable drug is not a bad drug — it is a *targeted* drug. It likely attacks a specific mutation that only certain cancers possess. This is the foundation of personalised medicine: find the mutation, match the drug.

---

### Step 3 — Cancer Cell Line Analysis
*Do certain cancers have a hidden weakness?*

Not all cancers are the same disease. A drug that cures lung cancer may do nothing to brain cancer, even though both are called "cancer." Here we group experiments by cancer type and cell line to find the most vulnerable combinations.

#### Most Sensitive Cancer Type + Drug Combinations

| Cancer Type | Drug | Mean LN_IC50 |
|------------|------|-------------|
| CLL | SN-38 | -6.780 |
| CLL | Vinorelbine | -6.724 |
| CLL | Romidepsin | -6.660 |
| LCML | Dasatinib | -6.575 |
| ALL | Daporinab | -6.527 |
| CLL | Docetaxel | -6.467 |
| MB | Daporinab | -6.421 |
| CLL | Rapamycin | -6.400 |
| ACC | Sepantronium bromide | -6.291 |

#### Most Sensitive Individual Cell Lines

| Cell Line | Drug | LN_IC50 |
|-----------|------|---------|
| MEG-01 | Dasatinib | -8.643 |
| NB14 | Daporinab | -8.620 |
| BV-173 | Dactinomycin | -8.574 |
| KU812 | Dasatinib | -8.564 |
| KELLY | Daporinab | -8.392 |

#### Biological Interpretation

The dominance of **CLL (Chronic Lymphocytic Leukaemia)** at the top of the sensitivity rankings is one of the most striking findings in our dataset. CLL cells appear across multiple drug categories in the top 10 most sensitive combinations — appearing with SN-38, Vinorelbine, Romidepsin, Docetaxel, and Rapamycin. This is not coincidence.

CLL is a blood cancer where white blood cells grow uncontrollably but remain in a relatively immature, "stuck" state. This biological immaturity makes them paradoxically *more* sensitive to many drugs — they lack the full suite of defensive mechanisms that more aggressive, differentiated tumours develop.

The combination of **LCML (Leukaemia) + Dasatinib** (LN_IC50 = -6.575) is particularly significant. Dasatinib is a BCR-ABL inhibitor — a drug specifically designed to target the abnormal protein produced by the "Philadelphia chromosome," a genetic mutation found in nearly all CML patients. Seeing LCML at the top of the Dasatinib sensitivity list is a direct **biological validation** of our analysis — the drug is working exactly as intended, on the cancer it was designed for.

**MEG-01** (LN_IC50 = -8.643 with Dasatinib) is a cell line derived from a CML patient, explaining its extraordinary sensitivity to Dasatinib. Similarly, NB14 and KELLY are neuroblastoma cell lines known to carry amplifications in the MYCN gene — a driver of aggressive growth that also creates specific drug vulnerabilities.

> **Biological insight:** The fact that leukaemia types (CLL, LCML, ALL) dominate the most-sensitive list reflects their biology — blood cancers are often more accessible to drug treatment than solid tumours, which can develop physical barriers and more complex resistance mechanisms.

---

### Step 4 — Genomic Influence on Drug Response
*Does your DNA determine whether a drug will work?*

This is where biology becomes truly remarkable. Cancer is, at its core, a disease of the genome — it starts when DNA is damaged or mutated. So we ask: **does the type of genetic damage in a cancer cell predict how it will respond to a drug?**

We investigate three types of genomic features using Spearman correlation against LN_IC50:

#### Correlation Results

| Genomic Feature | Correlation with LN_IC50 | Strength | Direction |
|----------------|--------------------------|----------|-----------|
| CNA (Copy Number Alteration) | -0.0067 | Very Weak / None | Sensitivity |
| Gene Expression | +0.0284 | Very Weak / None | Resistance |
| Methylation | +0.0024 | Very Weak / None | Resistance |

#### Biological Interpretation

The correlations are all very weak — close to zero — which at first glance might seem like a disappointing result. But this finding is itself a meaningful biological signal, and it deserves careful interpretation rather than dismissal.

**Why the correlations are weak — and what it means:**

The CNA, Gene Expression, and Methylation columns in this dataset are binary flags (Yes/No) applied at the *cell line level*, not at the individual gene level. They answer the question: "Does this cancer cell, in general, have copy number alterations?" — not "Does this specific gene have a copy number alteration relevant to this drug?"

When we ask whether *having any CNA at all* predicts drug sensitivity across *all drugs*, we are averaging over hundreds of drugs with completely different targets. A CNA in Gene X might make a cancer sensitive to Drug A but resistant to Drug B. These opposing effects cancel each other out when aggregated, producing a near-zero correlation.

**What this tells us biologically:**

1. **Genomic context is drug-specific.** The binary presence of CNA is not sufficient to predict sensitivity without knowing *which* gene is altered and *which* drug targets it. This is why precision oncology panels test for specific mutations, not just "any mutation."

2. **Gene Expression shows a tiny positive correlation (+0.028 towards resistance).** This hint — small as it is — is biologically plausible. Cancers with abnormally active genes tend to be more aggressive and have developed stronger survival mechanisms, making them slightly more resistant on average.

3. **Methylation's near-zero correlation (+0.002)** suggests that across all drugs, gene silencing by methylation neither consistently sensitises nor resists treatment. Again, the effect would likely be strong and drug-specific, but washes out at this aggregate level.

> **Biological insight:** This result does not mean genomics doesn't matter — it means genomics matters *specifically and contextually*. A BCR-ABL mutation predicts Dasatinib sensitivity with extraordinary precision. But BCR-ABL doesn't tell you anything about response to Paclitaxel. The lesson: genomic biomarkers must be matched to the right drug to unlock their predictive power.

---

### Step 5 — Visualising the Story
*A picture is worth a thousand data points.*

We created five visualisations to make our findings clear and accessible:

**1. Distribution Plot** (`distribution_plot.png`)
Shows the spread of all 162,103 LN_IC50 values. The distribution is roughly bell-shaped but right-skewed — meaning there are more experiments where drugs required high doses (less effective) than very low doses. The tail extends to +13.8 on the right (very resistant cancer cells) and -8.6 on the left (extremely sensitive ones).

**2. Boxplot — Top 10 Most Effective Drugs** (`boxplot_top_effective_drugs.png`)
Compares the spread of LN_IC50 values for the best-performing drugs. Romidepsin and Bortezomib show tight boxes (consistent across cancer types), while Daporinab and Docetaxel show wide boxes (highly variable — effective for some cancers, less so for others).

**3. Boxplot — Top 10 Most Sensitive Cancer Types** (`boxplot_cancer_types.png`)
Leukaemia types (CLL, ALL, LCML) cluster at the low end of LN_IC50, confirming their general drug sensitivity. This visual makes the clinical prioritisation immediately obvious — where should research and treatment attention focus first.

**4. Scatter Plot — AUC vs LN_IC50** (`scatter_auc_ic50.png`)
Shows a negative relationship: as LN_IC50 decreases (more potent drug), AUC also decreases (the cancer cells are inhibited more fully across all doses). The two metrics are correlated but not identical — some drugs have low LN_IC50 but moderate AUC, suggesting they hit hard at the target dose but taper off at higher concentrations.

**5. Correlation Heatmap** (`correlation_heatmap.png`)
The big picture view. LN_IC50 and AUC show a strong negative correlation (as expected — more effective drugs require lower concentrations and produce lower AUC). Z_SCORE correlates moderately with LN_IC50. The genomic features (CNA, Gene Expression, Methylation) show very weak correlations with all drug response metrics — consistent with our Step 4 findings.

---

## What Our Findings Mean — The Full Picture

Taken together, our analysis tells a coherent biological story:

**Cancer is not one disease.** The 2.84 standard deviation in LN_IC50 — nearly equal to the mean — confirms that different cancers respond to drugs in dramatically different ways. A treatment protocol designed for the "average cancer" will fail a large fraction of patients.

**Some drugs are broad weapons; others are precision tools.** Romidepsin and Bortezomib work well across nearly all cancer types because they target universal cellular machinery — DNA packaging and protein recycling — that all cancer cells depend on. Dasatinib and Gemcitabine are precision tools: highly effective when matched to the right target (BCR-ABL, rapidly dividing cells), nearly useless otherwise.

**Blood cancers are the most treatable in this dataset.** CLL dominates the most sensitive combinations. This aligns with clinical reality — blood cancers have historically shown better responses to systemic drug treatment than solid tumours, which develop physical barriers and complex resistance pathways.

**Genomics matters contextually, not globally.** The weak aggregate correlations do not mean genetics is irrelevant — they mean genetic biomarkers only predict drug response when matched to the right drug. This is the central principle of precision oncology, and our data supports it.

---

## Why This All Matters

Every year, millions of people are diagnosed with cancer. Many receive treatments that do not work — not because better drugs do not exist, but because we have not yet perfectly matched the right drug to the right patient.

Projects like GDSC, and analyses like ours, are building the scientific foundation for a future where a doctor can look at a tumour's genetic profile and say with confidence:

*"Based on the biology of your cancer, this is the drug most likely to help you."*

That future is not science fiction. It is what data-driven biology is actively constructing — one experiment, one dataset, one analysis at a time.

---

## The Code

```python
#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Column name constants
COL_CELL_LINE   = 'CELL_LINE_NAME'
COL_DRUG        = 'DRUG_NAME'
COL_TCGA_DESC   = 'TCGA_DESC'
COL_LN_IC50     = 'LN_IC50'
COL_AUC         = 'AUC'
COL_Z_SCORE     = 'Z_SCORE'
COL_CNA         = 'CNA'
COL_GENE_EXPR   = 'Gene Expression'
COL_METHYLATION = 'Methylation'
COL_TARGET_PATH = 'TARGET_PATHWAY'
COL_CANCER_TYPE = 'Cancer Type (matching TCGA label)'
COL_META_NAME   = 'Columns'

GENOMIC_FEATURES = [COL_CNA, COL_GENE_EXPR, COL_METHYLATION]
METRIC_COLS      = [COL_LN_IC50, COL_AUC, COL_Z_SCORE]
KEY_COLUMNS      = [COL_CELL_LINE, COL_DRUG, COL_TCGA_DESC, COL_LN_IC50, COL_AUC, COL_Z_SCORE,
                    COL_CNA, COL_GENE_EXPR, COL_METHYLATION, COL_TARGET_PATH]


def load_and_explore_data(p_datapath, p_metadatapath):
    """Load the GDSC dataset and perform initial exploration."""
    print(f"Loading data from {p_datapath}...\n")
    try:
        df_data = pd.read_excel(p_datapath)
        print("Dataset loaded successfully. Preview:")
        print(df_data.head())
    except Exception as e:
        print(f"Error loading the data file: {e}")
        return None

    print(f"Loading metadata from {p_metadatapath}...\n")
    try:
        df_metadata = pd.read_excel(p_metadatapath)
    except Exception as e:
        print(f"Error loading the metadata file: {e}")
        return None

    print("What are the key variables in the dataset? ")
    print(df_data[KEY_COLUMNS].head())
    print(f"Total Rows: {df_data.shape[0]}")
    print(f"Total Columns: {df_data.shape[1]}\n")

    print("What does each column represent (see metadata description)?")
    for _, row in df_metadata.iterrows():
        print(f"Column: {row[COL_META_NAME]}")
        for col_name in df_metadata.columns:
            if col_name != COL_META_NAME:
                print(f"  - {col_name}: {str(row[col_name])}")
        print("")

    print("Are there missing values or inconsistencies?")
    missing_values = df_data.isnull().sum()
    missing_cols = missing_values[missing_values > 0]
    if not missing_cols.empty:
        print(missing_cols)
    else:
        print("No missing values found!")

    print("\nChecking data types and non-null counts:")
    print(df_data.info())

    print("\nSummary statistics:")
    print(df_data.describe())

    print("\n--- Duplicates Check ---")
    duplicates = df_data.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}\n")

    return df_data


def analyze_drug_sensitivity(df):
    """Analyze which drugs are most/least effective and their variance."""
    print("\nAnalyzing drug sensitivity patterns...")
    if COL_DRUG not in df.columns or COL_LN_IC50 not in df.columns:
        print(f"  -> Missing '{COL_DRUG}' or '{COL_LN_IC50}' column. Skipping...")
        return

    drug_stats = df.groupby(COL_DRUG)[COL_LN_IC50].agg(['mean', 'std']).dropna()

    print("\nWhich drugs appear to be the most effective? (Lowest Mean) ---")
    print(drug_stats.sort_values(by='mean').head(10))
    print("\nWhich drugs show the least effectiveness? (Highest Mean) ---")
    print(drug_stats.sort_values(by='mean', ascending=False).head(10))
    print("\nAre there drugs with highly variable responses across cell lines? (Highest Std Dev) ---")
    print(drug_stats.sort_values(by='std', ascending=False).head(10))


def analyze_cell_line_response(df):
    """Analyze how cancer types and cell lines respond to treatments."""
    print("Do certain cancer types / cell lines respond better to specific drugs?")

    if COL_CANCER_TYPE in df.columns and COL_LN_IC50 in df.columns:
        cancer_drug_response = df.groupby([COL_CANCER_TYPE, COL_DRUG])[COL_LN_IC50].mean().sort_values().reset_index()
        print(f"\n--- Most Sensitive Cancer Types (Lowest Mean {COL_LN_IC50}) ---")
        print(cancer_drug_response.head(10))
    else:
        print(f"  -> Column '{COL_CANCER_TYPE}' not found. Cannot analyze cancer types.")

    if COL_CELL_LINE in df.columns and COL_LN_IC50 in df.columns:
        cell_drug_response = df.groupby([COL_CELL_LINE, COL_DRUG])[COL_LN_IC50].mean().sort_values().reset_index()
        print(f"\n--- Most Sensitive Cell Lines (Lowest Mean {COL_LN_IC50}) ---")
        print(cell_drug_response.head(10))

    print("\nWhat patterns exist in the drug response across cell lines?")
    if COL_DRUG in df.columns and COL_LN_IC50 in df.columns:
        drug_patterns = df.groupby(COL_DRUG)[COL_LN_IC50].agg(['mean', 'std']).dropna()
        print("Pattern 1: Universally Strong Drugs (Lowest Mean)")
        print(drug_patterns.sort_values('mean').head(10))
        print("Pattern 2: Highly Targeted Drugs (Highest Variance)")
        print(drug_patterns.sort_values('std', ascending=False).head(10))


def analyze_genomic_influence(df):
    """Analyze if genomic features influence drug response via Spearman correlation."""
    print("\nAre mutations (CNA), gene expression or methylation level influencing drug sensitivity at all?")

    existing_features = [col for col in GENOMIC_FEATURES if col in df.columns]
    if not existing_features:
        print("  -> Genomic feature columns not found in the dataset. Skipping analysis.")
        return
    if COL_LN_IC50 not in df.columns:
        print(f"  -> Metric column '{COL_LN_IC50}' not found. Skipping analysis.")
        return

    df_subset = df[[COL_LN_IC50] + existing_features].copy()
    for col in existing_features:
        df_subset[col] = df_subset[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
        df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')

    df_clean = df_subset.dropna()
    print(f"  -> Calculating correlations based on {len(df_clean)} complete records...\n")
    if len(df_clean) == 0:
        print("  -> No valid numeric data available for correlation. Check data formatting.")
        return

    correlations = df_clean.corr(method='spearman')[COL_LN_IC50].drop(COL_LN_IC50)

    print(f"--- Correlation with Drug Sensitivity ({COL_LN_IC50}) ---")
    print("Note: 'Y' (Present) was converted to 1, 'N' (Absent) to 0.")
    print("A Negative correlation means Presence of feature = LOWER LN_IC50 (Increased Sensitivity).")
    print("A Positive correlation means Presence of feature = HIGHER LN_IC50 (Increased Resistance).\n")

    for feature, corr_value in correlations.items():
        if abs(corr_value) < 0.2:
            strength = "Very Weak/None"
        elif abs(corr_value) < 0.4:
            strength = "Weak"
        elif abs(corr_value) < 0.6:
            strength = "Moderate"
        else:
            strength = "Strong"
        direction = "Resistance" if corr_value > 0 else "Sensitivity"
        print(f"{feature}: {corr_value:>7.4f} ({strength} correlation towards {direction})")

    return correlations


def visualize_results(df):
    """Generate and save supporting visualizations for the GDSC dataset."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    print(f"\nGenerating Data Visualizations and saving to: {output_dir}")

    if COL_LN_IC50 not in df.columns:
        print(f"  -> Column '{COL_LN_IC50}' not found. Cannot generate visualizations.")
        return

    sns.set_theme(style="whitegrid")

    print("  -> Saving 1/5: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[COL_LN_IC50].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({COL_LN_IC50})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency (Number of Cell Lines)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300)
    plt.close()

    print("  -> Saving 2/5: boxplot_top_effective_drugs.png...")
    if COL_DRUG in df.columns:
        plt.figure(figsize=(12, 6))
        drug_stats = df.groupby(COL_DRUG)[COL_LN_IC50].agg(['mean', 'std']).dropna()
        top_effective_drugs = drug_stats.sort_values('mean').head(10).index
        df_top_drugs = df[df[COL_DRUG].isin(top_effective_drugs)]
        sns.boxplot(data=df_top_drugs, x=COL_DRUG, y=COL_LN_IC50, hue=COL_DRUG,
                    palette="Set2", order=top_effective_drugs, legend=False)
        plt.title(f'Drug Sensitivity ({COL_LN_IC50}) Across Top 10 Most Effective Drugs', fontsize=14, fontweight='bold')
        plt.xlabel('Drug Name', fontsize=12)
        plt.ylabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "boxplot_top_effective_drugs.png"), dpi=300)
        plt.close()
    else:
        print(f"  -> '{COL_DRUG}' not found. Skipping boxplot.")

    print("  -> Saving 3/5: boxplot_cancer_types.png...")
    if COL_CANCER_TYPE in df.columns:
        plt.figure(figsize=(14, 6))
        cancer_means = df.groupby(COL_CANCER_TYPE)[COL_LN_IC50].mean().sort_values().head(10).index
        df_top_cancers = df[df[COL_CANCER_TYPE].isin(cancer_means)]
        sns.boxplot(data=df_top_cancers, x=COL_CANCER_TYPE, y=COL_LN_IC50, hue=COL_CANCER_TYPE,
                    palette="Set3", order=cancer_means, legend=False)
        plt.title(f'Drug Sensitivity ({COL_LN_IC50}) Across Top 10 Most Sensitive Cancer Types', fontsize=14, fontweight='bold')
        plt.xlabel('Cancer Type', fontsize=12)
        plt.ylabel(f'{COL_LN_IC50} (Lower = More Sensitive)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "boxplot_cancer_types.png"), dpi=300)
        plt.close()
    else:
        print(f"  -> '{COL_CANCER_TYPE}' not found. Skipping cancer type boxplot.")

    print("  -> Saving 4/5: scatter_auc_ic50.png...")
    if COL_AUC in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=COL_AUC, y=COL_LN_IC50, alpha=0.5, color='darkorange')
        plt.title(f'Relationship between {COL_AUC} and {COL_LN_IC50}', fontsize=14, fontweight='bold')
        plt.xlabel('AUC (Area Under the Curve)', fontsize=12)
        plt.ylabel(COL_LN_IC50, fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50.png"), dpi=300)
        plt.close()
    else:
        print(f"  -> '{COL_AUC}' column not found. Skipping scatter plot.")

    print("  -> Saving 5/5: correlation_heatmap.png...")
    df_heat = pd.DataFrame()
    for col in METRIC_COLS:
        if col in df.columns:
            df_heat[col] = df[col]
    for col in GENOMIC_FEATURES:
        if col in df.columns:
            df_heat[col] = df[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
            df_heat[col] = pd.to_numeric(df_heat[col], errors='coerce')

    plt.figure(figsize=(10, 8))
    if not df_heat.empty and len(df_heat.columns) > 1:
        corr_matrix = df_heat.corr(method='spearman')
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1,
                    square=True, linewidths=.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Heatmap of Biological Variables', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=300)
        plt.close()
    else:
        print("  -> Not enough valid biological columns to generate a correlation heatmap.")


def main():
    print("Welcome to HackBio: GDSC Data Analysis Project!")
    print("Investigating Genomics of Drug Sensitivity in Cancer...\n")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path     = os.path.join(base_dir, "data", "GDSC.xlsx")
    metadata_path = os.path.join(base_dir, "data", "metadata.xlsx")

    print("Part 1: Understanding the dataset starts...\n")
    df = load_and_explore_data(data_path, metadata_path)
    print("Part 1: Understanding the dataset completes.\n")

    if df is not None:
        print("Part 2: Drug Sensitivity patterns starts...\n")
        analyze_drug_sensitivity(df)
        print("Part 2: Drug Sensitivity patterns completes.\n")

        print("Part 3: Cancer cell line analysis starts...\n")
        analyze_cell_line_response(df)
        print("Part 3: Cancer cell line analysis completes.\n")

        print("Part 4: Genomic influence analysis starts...\n")
        analyze_genomic_influence(df)
        print("Part 4: Genomic influence analysis completes.\n")

        print("Part 5: Supporting Data Visualization starts...\n")
        visualize_results(df)
        print("Part 5: Supporting Data Visualization completes.\n")

        print("\nHackBio GDSC Data Analysis Project Complete!")


if __name__ == "__main__":
    main()
```

---

*Dataset source: Genomics of Drug Sensitivity in Cancer (GDSC), a public scientific database maintained for cancer pharmacogenomics research.*

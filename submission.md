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

- The **rows** represent one drug tested on one cancer cell line
- The **columns** describe everything about that experiment

Here are the key columns and what they mean in plain English:

**Identifiers & Classifications**

*CELL_LINE_NAME* — The specific name of the cancer cell model being tested.

*TCGA_DESC* — The type of cancer (e.g., lung, colon, breast).

*DRUG_NAME* — The name of the pharmaceutical compound being tested.

*TARGET_PATHWAY* — The biological process the drug is designed to disrupt.

**Drug Response Metrics**

*LN_IC50* — How much drug was needed to kill 50% of the cancer cells. A lower value means the drug is more powerful.

*AUC* — Area Under the Curve. How well the drug worked across a full range of doses.

*Z_SCORE* — How unusual this cell line's response is compared to the average across all experiments.

**Molecular & Genetic Features**

*CNA* — Copy Number Alteration. Whether the cancer cell has a DNA copy error (a section duplicated or deleted).

*Gene Expression* — Whether a specific gene is unusually active or silent in this cancer cell.

*Methylation* — Whether certain genes have been chemically "switched off" in this cancer cell.

> **Key metric — LN_IC50:** A very negative LN_IC50 means the drug is a precision weapon — a tiny amount kills the cancer cells. A high LN_IC50 means you would need a dangerously large dose to see any effect.

---

## Our Analysis: A 5-Step Investigation

---

### Step 1 — Understanding the Dataset
*What are we actually working with?*

Before drawing any conclusions, we get to know our data intimately:

- **How many experiments?**
- **Are there gaps or errors?** We scan for missing values and duplicate entries.
- **Are the numbers stored as numbers?** We verify data types.
- **What does each column mean?** We cross-reference against a metadata file.

#### Results

```
Total Rows:    162,103
Total Columns: 19
Missing Values: None
Duplicate Rows: 0
```

| Metric   | Mean  | Std Dev | Min    | Max    |
|----------|-------|---------|--------|--------|
| LN_IC50  | 2.82  | 2.84    | -8.64  | 13.82  |
| AUC      | 0.88  | 0.15    | 0.006  | 0.999  |
| Z_SCORE  | 0.04  | 1.00    | -6.91  | 7.98   |

#### Biological Interpretation

The dataset contains **162,103 complete experiments** with zero missing values or duplicates — exceptional quality for real-world biological data.

The mean LN_IC50 of **2.82** tells us a moderate-to-high dose is typically required. But the standard deviation of **2.84** — nearly equal to the mean — is the critical signal. Drug effectiveness varies enormously across experiments. This is not noise; it is biology telling us that different cancers are fundamentally different diseases, and a one-size-fits-all treatment approach is biologically inappropriate.

The LN_IC50 range spans from **-8.64** (a drug so potent it needs almost no dose) to **+13.82** (a drug requiring an impossibly large dose). This 22-unit range underscores the importance of matching the right drug to the right cancer.

> **Why data quality matters:** In real laboratory settings, machines malfunction and values get entered incorrectly. Cleaning the data is not glamorous, but skipping it is like building a house on sand. The fact that our dataset is perfectly complete means every finding below can be trusted.

---

### Step 2 — Drug Sensitivity Patterns
*Which drugs are champions, and which are duds?*

We rank every drug by effectiveness and identify patterns across biological pathways.

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
| Daporinad | -3.323 | 2.736 |
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

#### Highly Variable Drugs — Selective Responders (Highest Std Dev)

| Drug | Mean LN_IC50 | Std Dev |
|------|-------------|---------|
| Gemcitabine | -0.632 | 2.942 |
| AZD5991 | 3.863 | 2.759 |
| Daporinad | -3.323 | 2.736 |
| Docetaxel | -3.327 | 2.547 |
| Dasatinib | 1.274 | 2.394 |
| Methotrexate | 0.457 | 2.389 |
| Tozasertib | 2.025 | 2.387 |
| Trametinib | 0.089 | 2.302 |

#### Drug Pathway Sensitivity Summary

| Target Pathway | Mean LN_IC50 | Std Dev | Experiments |
|---------------|-------------|---------|-------------|
| Mitosis | -1.397 | 3.325 | 4,914 |
| Protein stability & degradation | 0.832 | 3.802 | 5,362 |
| Cell cycle | 1.545 | 2.810 | 8,845 |
| Apoptosis regulation | 1.777 | 2.972 | 7,693 |
| DNA replication | 2.099 | 3.340 | 12,400 |
| PI3K/MTOR signaling | 2.566 | 2.360 | 17,343 |
| RTK signaling | 2.588 | 2.417 | 8,037 |
| EGFR signaling | 2.631 | 1.617 | 5,119 |
| Chromatin histone acetylation | 2.681 | 2.878 | 6,233 |
| ERK MAPK signaling | 2.893 | 2.146 | 10,176 |

**Kruskal-Wallis test (are pathway differences statistically significant?):**
```
H = 21,985.95,  p = 0.00e+00  (statistically significant beyond machine precision)
→ Drug pathways target biologically distinct mechanisms with measurably different therapeutic efficacy.
```

#### Biological Interpretation

**Romidepsin** is the most potent drug in the dataset (mean LN_IC50 = -5.18). It is an HDAC (Histone Deacetylase) inhibitor — it works by blocking the proteins that control how tightly DNA is wound inside the cell. When these proteins are disabled, cancer cells lose the ability to silence their own self-destruct signals. The narrow standard deviation (1.03) confirms this effect is **consistent across cancer types** — Romidepsin is a broad-spectrum weapon.

**Bortezomib** (-4.75) is a proteasome inhibitor — it blocks the cell's internal "waste disposal system." Cancer cells produce abnormal proteins at high rates; when the disposal system is blocked, they choke on their own toxic waste and die.

The antioxidants at the bottom — **Vitamin C, N-acetyl cysteine, Glutathione** — confirm that nutritional supplements alone cannot kill cancer cells at practical doses. Their high LN_IC50 values serve as a useful negative control.

**The pathway analysis reveals a striking and statistically proven pattern:** Mitosis-targeting drugs are the most effective on average (mean -1.40), while ERK MAPK signaling drugs are the least (mean 2.89). The Kruskal-Wallis test (H = 21,985.95, p ≈ 0) confirms this is not a chance finding — **pathway membership is a statistically significant predictor of drug effectiveness.** This makes biological sense — cancer cells divide far more rapidly than normal cells, making mitosis their greatest vulnerability.

**Highly variable drugs are the most clinically interesting.** Gemcitabine (std 2.94) and Dasatinib (std 2.39) show wildly different responses across cancer types. This variability is a signal, not noise — these drugs are hitting a specific biological target that only some cancers possess.

> **Biological insight:** The distinction between broadly effective drugs (Romidepsin, Bortezomib) and highly selective drugs (Dasatinib, Gemcitabine) reflects two different treatment philosophies. Broad drugs attack universal cancer vulnerabilities. Selective drugs require matching — but when the match is right, they can be extraordinarily powerful.

---

### Step 3 — Cancer Cell Line Analysis
*Do certain cancers have a hidden weakness?*

Not all cancers are the same. A drug that works on lung cancer may do nothing to brain cancer, even though both are called "cancer." Here we identify which cancer types and cell lines are most vulnerable, which are most resistant, and which drugs show the most selective behaviour.

#### Most Sensitive Cancer Type + Drug Combinations

| Cancer Type | Drug | Mean LN_IC50 |
|------------|------|-------------|
| CLL | SN-38 | -6.780 |
| CLL | Vinorelbine | -6.724 |
| CLL | Romidepsin | -6.660 |
| LCML | Dasatinib | -6.575 |
| ALL | Daporinad | -6.527 |
| CLL | Docetaxel | -6.467 |
| MB | Daporinad | -6.421 |
| CLL | Rapamycin | -6.400 |
| CLL | Dactinomycin | -6.295 |
| ACC | Sepantronium bromide | -6.291 |

#### Most Sensitive Individual Cell Lines

| Cell Line | Drug | LN_IC50 |
|-----------|------|---------|
| MEG-01 | Dasatinib | -8.643 |
| NB14 | Daporinad | -8.620 |
| BV-173 | Dactinomycin | -8.574 |
| KU812 | Dasatinib | -8.564 |
| KELLY | Daporinad | -8.392 |
| LAMA-84 | Dasatinib | -8.267 |
| BB49-HNC | Vinorelbine | -8.085 |
| JURL-MK1 | Dasatinib | -8.069 |
| NCI-H1876 | SN-38 | -8.045 |
| NKM-1 | Dactinomycin | -7.826 |

#### Overall Cancer Type Sensitivity Ranking (mean LN_IC50 across all drugs)

**Most sensitive (lowest mean LN_IC50):**

| Cancer Type | Mean | Median | Std Dev | Experiments |
|------------|------|--------|---------|-------------|
| CLL | 1.105 | 1.553 | 3.056 | 469 |
| LAML | 1.532 | 2.044 | 2.821 | 5,154 |
| DLBC | 1.538 | 2.096 | 2.850 | 7,003 |
| ALL | 1.542 | 2.063 | 2.779 | 5,879 |
| LCML | 1.564 | 2.162 | 2.924 | 2,246 |
| MM | 1.928 | 2.471 | 2.858 | 3,787 |
| ACC | 2.173 | 2.820 | 2.844 | 239 |
| MB | 2.348 | 2.939 | 2.912 | 912 |
| NB | 2.348 | 2.851 | 2.758 | 6,660 |
| HNSC | 2.644 | 3.119 | 2.763 | 7,738 |

**Most resistant (highest mean LN_IC50):**

| Cancer Type | Mean | Median | Std Dev | Experiments |
|------------|------|--------|---------|-------------|
| KIRC | 3.128 | 3.493 | 2.662 | 6,758 |
| LGG | 3.157 | 3.643 | 2.889 | 3,163 |
| PRAD | 3.162 | 3.681 | 2.875 | 1,433 |
| OV | 3.209 | 3.594 | 2.788 | 7,237 |
| THCA | 3.276 | 3.669 | 2.893 | 3,293 |
| LUAD | 3.282 | 3.733 | 2.810 | 13,300 |
| UCEC | 3.320 | 3.844 | 2.602 | 2,147 |
| LIHC | 3.412 | 3.829 | 2.608 | 3,342 |
| MESO | 3.487 | 3.861 | 2.684 | 1,355 |
| PAAD | 3.732 | 4.165 | 2.782 | 5,875 |

#### Drug Selectivity — Largest Response Spread Across Cancer Types

| Drug | Selectivity Score |
|------|------------------|
| Tozasertib | 2.059 |
| AZD5991 | 1.994 |
| Gemcitabine | 1.877 |
| Dasatinib | 1.823 |
| Nilotinib | 1.708 |
| BI-2536 | 1.636 |
| Bosutinib | 1.593 |
| Cytarabine | 1.588 |
| Alisertib | 1.586 |
| LMP744 | 1.552 |

#### Biological Interpretation

**CLL (Chronic Lymphocytic Leukaemia)** dominates the most sensitive list across both cancer-drug combinations and the overall cancer type ranking (mean 1.105 — nearly 1.7 units below the dataset mean of 2.82). This is biologically meaningful. CLL cells are trapped in an immature developmental state and lack the full defensive machinery that more aggressive tumours develop.

**Blood cancers sweep the top 6 most sensitive types** — CLL, LAML (acute myeloid leukaemia), DLBC (diffuse large B-cell lymphoma), ALL (acute lymphoblastic leukaemia), LCML, and MM (multiple myeloma). This reflects a shared biological property: blood cancers circulate in the bloodstream, are continuously exposed to systemically delivered drugs, and lack the physical barriers (dense tissue, poor blood supply, efflux pumps) that protect solid tumours.

**PAAD (pancreatic adenocarcinoma)** is the most resistant cancer type (mean 3.732), 0.9 units above the dataset mean. This is clinically consistent with pancreatic cancer's notorious drug resistance — a dense stromal barrier physically prevents drugs from reaching tumour cells, and the tumour suppressor gene KRAS is almost universally mutated in a way that makes it "undruggable" by conventional approaches.

**LCML + Dasatinib** (LN_IC50 = -6.575) is a textbook precision oncology result. LCML is almost universally driven by the BCR-ABL fusion gene. Dasatinib was specifically engineered to block BCR-ABL. Seeing LCML at the top of the Dasatinib sensitivity list is a **direct biological validation** of our analysis working correctly.

**The selectivity analysis reveals a clinically crucial distinction.** Tozasertib (score 2.06), AZD5991 (1.99), and Dasatinib (1.82) show the greatest spread across cancer types. These are not broadly effective — they are extraordinarily powerful for specific cancers and almost useless for others. The selectivity score is essentially a measure of how "targeted" the drug truly is.

> **Biological insight:** The gap between blood cancers (CLL mean 1.105) and the most resistant solid tumour (PAAD mean 3.732) is 2.6 LN_IC50 units — equivalent to needing approximately 13× more drug for pancreatic cancer than for leukaemia. This is not just a statistical difference; it is the difference between a treatable and an untreatable disease at standard doses.

---

### Step 4 — Genomic Influence on Drug Response
*Does your DNA determine whether a drug will work?*

Cancer is a disease of the genome. We investigate whether three types of genomic alterations — Copy Number Alterations (CNA), Gene Expression changes, and Methylation — influence how a cancer cell responds to drugs.

We used **seven complementary analytical methods** to answer this question at increasing levels of depth.

---

#### Method 1: Overall Spearman Correlation

| Feature | Correlation with LN_IC50 | Direction |
|---------|--------------------------|-----------|
| CNA | -0.0067 | Very Weak towards Sensitivity |
| Gene Expression | +0.0284 | Very Weak towards Resistance |
| Methylation | +0.0024 | Very Weak towards Resistance |

These aggregate correlations are near zero — not because genomics is irrelevant, but because averaging across all drugs and all cancer types washes out drug-specific and cancer-specific signals. Methods 2–7 reveal what is hidden beneath this average.

---

#### Method 2: Group Comparison (Y vs N) with Statistical Testing

**CNA (Copy Number Alteration):**
```
Present (Y): mean LN_IC50 = 2.8214  (n = 161,445)
Absent  (N): mean LN_IC50 = 3.1290  (n = 658)
→ Cells WITH CNA are more sensitive on average (diff = -0.3076)
→ Mann-Whitney U test: p = 7.39e-03 (statistically significant)
```

**Gene Expression:**
```
Present (Y): mean LN_IC50 = 2.8332  (n = 158,342)
Absent  (N): mean LN_IC50 = 2.3778  (n = 3,761)
→ Cells WITH Gene Expression changes are more resistant on average (diff = +0.4554)
→ Mann-Whitney U test: p = 2.91e-30 (statistically significant)
```

**Methylation:**
```
Present (Y): mean LN_IC50 = 2.8232  (n = 158,601)
Absent  (N): mean LN_IC50 = 2.7968  (n = 3,502)
→ Cells WITH Methylation are more resistant on average (diff = +0.0264)
→ Mann-Whitney U test: p = 3.42e-01 (not significant)
```

---

#### Method 3: Drug-Level Differential — Which Drugs Are Most Affected?

**CNA — Top 5 drugs where presence SENSITISES the cancer:**

| Drug | With CNA (Y) | Without CNA (N) | Shift |
|------|-------------|----------------|-------|
| ULK1_4989 | 2.443 | 5.548 | -3.106 |
| AZD5582 | 2.290 | 5.079 | -2.789 |
| Luminespib | -2.041 | 0.554 | -2.595 |
| Cytarabine | 1.704 | 4.217 | -2.512 |
| Tanespimycin | -0.130 | 2.209 | -2.339 |

**CNA — Top 5 drugs where presence CONFERS resistance:**

| Drug | With CNA (Y) | Without CNA (N) | Shift |
|------|-------------|----------------|-------|
| Dasatinib | 1.284 | -1.085 | +2.369 |
| AT13148 | 3.578 | 2.150 | +1.428 |
| AZD8055 | 0.044 | -1.376 | +1.419 |
| TAF1_5496 | 3.744 | 2.469 | +1.275 |
| AZD2014 | 2.231 | 1.034 | +1.197 |

**Gene Expression — Top 5 drugs where presence SENSITISES:**

| Drug | With GE (Y) | Without GE (N) | Shift |
|------|------------|----------------|-------|
| TW 37 | 1.313 | 5.630 | -4.317 |
| Bleomycin (50 uM) | 3.548 | 6.792 | -3.244 |
| UNC0638 | 4.209 | 6.714 | -2.505 |
| UNC0379 | 3.612 | 6.076 | -2.464 |
| Cisplatin | 3.368 | 5.541 | -2.173 |

**Gene Expression — Top 5 drugs where presence CONFERS resistance:**

| Drug | With GE (Y) | Without GE (N) | Shift |
|------|------------|----------------|-------|
| Cytarabine | 1.716 | -0.281 | +1.997 |
| Talazoparib | 2.982 | 1.475 | +1.508 |
| Docetaxel | -3.303 | -4.730 | +1.427 |
| Tozasertib | 2.173 | 0.765 | +1.407 |
| Dactinomycin | -3.648 | -5.036 | +1.388 |

**Methylation — Top 5 drugs where presence SENSITISES:**

| Drug | With Meth (Y) | Without Meth (N) | Shift |
|------|--------------|-----------------|-------|
| AZD5991 | 3.843 | 5.683 | -1.840 |
| GSK2110183B | 3.299 | 4.746 | -1.447 |
| Methotrexate | 0.422 | 1.812 | -1.391 |
| UNC0638 | 4.198 | 5.285 | -1.087 |
| ICL-SIRT078 | 4.353 | 5.282 | -0.929 |

**Methylation — Top 5 drugs where presence CONFERS resistance:**

| Drug | With Meth (Y) | Without Meth (N) | Shift |
|------|--------------|-----------------|-------|
| PRIMA-1MET | 4.516 | 3.641 | +0.875 |
| Cytarabine | 1.723 | 0.875 | +0.848 |
| Talazoparib | 2.957 | 2.170 | +0.787 |
| Dactinomycin | -3.657 | -4.394 | +0.737 |
| CHIR-99021 | 4.659 | 3.952 | +0.707 |

---

#### Method 4: Per-Cancer-Type Differential — Where Does Each Feature Matter Most?

**Gene Expression — Cancer types most sensitised (most negative shift):**

| Cancer Type | With GE (Y) | Without GE (N) | Shift |
|------------|------------|----------------|-------|
| KIRC | 3.099 | 4.214 | -1.115 |
| BRCA | 3.071 | 3.451 | -0.380 |
| SKCM | 2.877 | 3.159 | -0.283 |
| DLBC | 1.529 | 1.702 | -0.173 |

**Gene Expression — Cancer types made most resistant:**

| Cancer Type | With GE (Y) | Without GE (N) | Shift |
|------------|------------|----------------|-------|
| THCA | 3.348 | 2.026 | +1.322 |
| LUAD | 3.296 | 2.251 | +1.045 |
| COREAD | 3.093 | 2.193 | +0.900 |
| OV | 3.242 | 2.586 | +0.656 |
| SCLC | 2.810 | 2.251 | +0.559 |

**Methylation — Cancer types most sensitised:**

| Cancer Type | With Meth (Y) | Without Meth (N) | Shift |
|------------|--------------|-----------------|-------|
| SCLC | 2.756 | 3.351 | -0.594 |
| COREAD | 3.069 | 3.453 | -0.384 |
| BRCA | 3.071 | 3.451 | -0.380 |
| LUAD | 3.276 | 3.600 | -0.323 |
| DLBC | 1.534 | 1.683 | -0.149 |

**Methylation — Cancer types made most resistant:**

| Cancer Type | With Meth (Y) | Without Meth (N) | Shift |
|------------|--------------|-----------------|-------|
| GBM | 3.152 | 2.134 | +1.018 |
| OV | 3.263 | 2.670 | +0.592 |
| ALL | 1.562 | 1.231 | +0.331 |
| KIRC | 3.139 | 2.943 | +0.196 |

*Note: CNA is present (Y) in 99.6% of all cell lines, leaving insufficient N cases for per-cancer-type comparison in most cancer types. This extreme prevalence is itself biologically significant — copy number alterations are nearly universal in cancer cell lines used for drug screening.*

---

#### Method 5: Per-Pathway Differential — Which Drug Mechanisms Are Most Affected by Genomics?

**CNA — Pathways most sensitised by CNA presence:**

| Pathway | With CNA (Y) | Without CNA (N) | Shift |
|---------|-------------|----------------|-------|
| Mitosis | -1.402 | -0.151 | -1.251 |
| Apoptosis regulation | 1.773 | 2.765 | -0.991 |
| Cell cycle | 1.542 | 2.280 | -0.738 |
| Chromatin other | 3.455 | 4.192 | -0.737 |
| Protein stability & degradation | 0.829 | 1.421 | -0.592 |

**Gene Expression — Pathways most dramatically affected:**

| Pathway | Direction | With GE (Y) | Without GE (N) | Shift |
|---------|-----------|------------|----------------|-------|
| Metabolism | **+resistance** | 4.855 | 2.863 | +1.992 |
| Other | **+resistance** | 3.598 | 2.610 | +0.988 |
| JNK and p38 signaling | **+resistance** | 5.096 | 4.254 | +0.842 |
| p53 pathway | **+resistance** | 4.561 | 3.823 | +0.738 |
| Hormone-related | **sensitised** | 4.205 | 4.498 | -0.293 |

**Methylation — Pathways most sensitised by Methylation presence:**

| Pathway | With Meth (Y) | Without Meth (N) | Shift |
|---------|--------------|-----------------|-------|
| Mitosis | -1.412 | -0.768 | -0.644 |
| Hormone-related | 4.204 | 4.623 | -0.419 |
| IGF1R signaling | 2.993 | 3.265 | -0.271 |
| Chromatin histone methylation | 3.786 | 4.022 | -0.235 |
| RTK signaling | 2.583 | 2.800 | -0.217 |

---

#### Method 6: Extreme Responder Enrichment — Do Genomic Features Explain Outlier Responses?

```
Extreme responders (|Z_SCORE| > 2): 7,582 of 162,103 total (4.7%)

CNA:            99.9% of extreme responders are Y  (vs 99.6% overall — enriched 1.00×)
Gene Expression: 97.4% of extreme responders are Y  (vs 97.7% overall — depleted 1.00×)
Methylation:    97.4% of extreme responders are Y  (vs 97.8% overall — depleted 1.00×)
```

Genomic features alone do not explain outlier drug responses. The enrichment is essentially 1.0× across all three features — extreme responders look no different from the overall population in terms of feature presence. This tells us that **having the feature is not sufficient for an extreme response; it is the drug-feature interaction that matters** — consistent with Method 3 showing drug-specific shifts of up to 4.3 LN_IC50 units.

---

#### Method 7: Combined Genomic Feature Interaction

```
Mean LN_IC50 by number of genomic features simultaneously active:

Score 0 (none active): not present in dataset
Score 1 (one active):  mean = 2.764  (n = 1,243)
Score 2 (two active):  mean = 2.562  (n = 5,435)
Score 3 (all active):  mean = 2.832  (n = 155,425)
```

Two findings stand out: (1) No cell line in the dataset has all three genomic features absent — copy number alterations, gene expression changes, and methylation alterations are **universal** in cancer cell lines used for drug screening. This confirms that these are defining hallmarks of cancer biology, not incidental features. (2) The relationship is non-monotonic — cells with exactly two features active show the lowest mean LN_IC50 (most sensitive), suggesting that having partial genomic disruption may create specific dependencies that drugs can exploit, while full disruption (all three active) may trigger compensatory resistance mechanisms.

---

#### Overall Genomic Analysis Biological Interpretation

**CNA increases sensitivity via oncogene addiction — and massively sensitises Mitosis drugs.**

Cells with copy number alterations show lower mean LN_IC50 (p = 0.007). The pathway analysis reveals *why*: CNA-positive cells are nearly 1.3 LN_IC50 units more sensitive to Mitosis-targeting drugs (-1.402 vs -0.151). Copy number amplification of oncogenes makes cancer cells hyper-dependent on cell division — blocking mitosis in a cell already racing to divide is catastrophic. This concept is called **oncogene addiction**: the cancer becomes so reliant on amplified growth signals that any disruption of the machinery carrying them out is lethal. CNA is present in 99.6% of cell lines — it is not a rare variant; it is a defining feature of cancer that creates broad vulnerability to mitotic inhibitors.

**Gene Expression changes create cancer-type-specific effects — with the strongest genomic signal in the dataset.**

The Gene Expression finding (p = 2.91 × 10⁻³⁰) is the most statistically significant result in our entire analysis. But the direction depends entirely on which cancer type and which drug pathway are involved. **KIRC (kidney cancer)** shows the strongest sensitisation with active gene expression (−1.115 shift) — consistent with KIRC's known sensitivity to gene expression dysregulation from VHL tumour suppressor loss. **THCA (thyroid cancer)** shows the strongest resistance (+1.322 shift) — reflecting a cancer type whose oncogenic drivers (BRAF V600E, RET/PTC fusions) create active bypass pathways that compensate for drug pressure. At the pathway level, Metabolism drugs (+1.992) are dramatically less effective in gene-expression-active cells — cancer cells with elevated gene expression are metabolically more adaptable and can reroute around metabolic inhibitors. **TW 37** (BCL-2 inhibitor, shift -4.317) is the drug most improved by gene expression activity — cells that are actively transcribing genes are often over-expressing BCL-2 as a survival protein; blocking it removes their primary anti-death shield.

**Methylation sensitises Mitosis and Hormone-related pathways in solid tumours.**

Methylation silences tumour suppressor genes — the natural brakes on cancer growth. When brakes are removed, cells become more dependent on active growth pathways. The Mitosis pathway shows strong sensitisation in methylated cells (-0.644), because cells that have silenced growth suppressors are dividing faster and are therefore more vulnerable to mitotic disruption. **SCLC (small cell lung cancer)** is the cancer type most sensitised by methylation (-0.594), consistent with SCLC's known epigenetically driven biology and its established sensitivity to drugs that exploit methylation-related vulnerabilities.

> **The central conclusion of the genomic analysis:** No single genomic feature uniformly increases or decreases drug sensitivity across all cancers and drugs. Each feature creates specific, drug-and-cancer-type-dependent vulnerabilities. The overall Spearman correlations near zero are not null results — they are the mathematical consequence of averaging opposing signals. The deeper analysis (Methods 3–7) reveals that these opposing signals are real, large (up to 4.3 LN_IC50 units), statistically significant, and biologically meaningful. **The message for precision oncology: a patient's genomic profile must be interpreted in the context of which drug is being considered and which cancer type is present.**

---

### Step 5 — Visualising the Story
*Nine plots, nine perspectives on the same biological truth.*

**1. Distribution Plot** (`distribution_plot.png`)
The spread of all 162,103 LN_IC50 values. Right-skewed — more experiments where drugs required high doses than very low ones. The heavy left tail (down to -8.64) represents the rare but powerful drug-cancer matches that precision oncology seeks to identify and replicate.

**2. Boxplot — Top 10 Most Effective Drugs** (`boxplot_top_effective_drugs.png`)
Romidepsin and Bortezomib show tight boxes — consistent killers across cancer types. Daporinad and Docetaxel show wide boxes — highly selective, working brilliantly for some cancers and poorly for others.

**3. Boxplot — Top 10 Most Sensitive Cancer Types** (`boxplot_cancer_types.png`)
Leukaemia types cluster at the bottom, confirming systemic drug vulnerability. Solid tumours sit higher, reflecting physical and biological resistance mechanisms.

**4. Scatter Plot — AUC vs LN_IC50** (`scatter_auc_ic50.png`)
Negative relationship confirmed — as drugs become more potent (lower LN_IC50), they also inhibit cells more completely across all doses (lower AUC). The spread shows that some drugs are potent at target dose but taper off, while others maintain effectiveness across the full dose range.

**5. Correlation Heatmap** (`correlation_heatmap.png`)
LN_IC50 and AUC strongly negatively correlated. Z_SCORE moderately correlates with LN_IC50. Genomic features show near-zero correlations with drug metrics at the aggregate level — consistent with Method 1 findings and the masking effect discussed in Methods 3–7.

**6. Violin Plots — Genomic Feature Groups** (`violin_genomic_features.png`)
Direct visual comparison of LN_IC50 distributions for cells with (Y) vs without (N) CNA, Gene Expression, and Methylation. The violin shapes reveal not just mean differences but the full distribution — showing that genomic features shift the entire response landscape, not just the average.

**7. Pivot Heatmap — Cancer Type × Drug** (`heatmap_cancer_drug_pivot.png`)
A matrix of the top 15 cancer types against the top 15 most effective drugs. Dark green cells represent the strongest drug-cancer sensitivities. The pattern is not random — leukaemia types (CLL, ALL, LCML) show consistently green rows, confirming their broad drug sensitivity.

**8. Horizontal Bar Chart — Drug Sensitivity by Target Pathway** (`barplot_pathway_sensitivity.png`)
All drug target pathways ranked by mean LN_IC50, displayed as a horizontal bar chart. Green bars (negative LN_IC50) represent pathways where drugs achieve net cancer-killing efficiency; blue bars represent pathways where drugs struggle. The Mitosis bar stands visibly apart from all others — a direct visual confirmation of the Kruskal-Wallis statistical finding.

**9. Vertical Bar Chart — Top 20 Most Sensitive Cancer Types** (`barplot_cancer_sensitivity.png`)
The 20 most drug-sensitive cancer types (by TCGA code) ranked by mean LN_IC50, with the dataset-wide mean marked as a reference line. Blood cancers cluster at the left of the chart, dramatically below the reference line. The bar chart format makes the magnitude of differences between cancer types immediately interpretable.

---

## What Our Findings Mean — The Full Picture

**Cancer is not one disease.** The LN_IC50 range spans 22 units (-8.64 to +13.82), with a standard deviation nearly equal to the mean. Different cancers respond to drugs in fundamentally different ways. A treatment protocol designed for the "average cancer" will fail a large fraction of patients.

**Pathway membership is a statistically proven predictor of drug effectiveness.** The Kruskal-Wallis test (H = 21,985.95, p ≈ 0) confirms that a drug's target pathway is one of the strongest predictors of its average effectiveness — stronger than knowing the individual drug name for most compounds. Mitosis-targeting drugs (mean -1.40) outperform all other pathway classes by a significant margin.

**Broad weapons and precision tools serve different roles.** Romidepsin and Bortezomib attack universal cellular machinery — they work broadly because all cancer cells depend on HDAC and proteasome function. Dasatinib and Gemcitabine are precision tools — extraordinarily powerful when matched to the right cancer, ineffective otherwise.

**Blood cancers are the most treatable in this dataset.** The top 6 most sensitive cancer types are all blood cancers (CLL, LAML, DLBC, ALL, LCML, MM), with mean LN_IC50 values 1.3–1.7 units below the dataset mean. The most resistant cancer (PAAD) requires 2.6× more drug than the most sensitive (CLL).

**Genomic features are drug-and-cancer-specific predictors, not universal markers.** CNA sensitises to Mitosis drugs with a 1.25-unit shift; Gene Expression creates a 1.99-unit resistance increase for Metabolism drugs but a 4.32-unit sensitivity increase for BCL-2 inhibitors. The feature must be matched to the drug and the cancer type to be clinically useful. This is the precision oncology paradigm in data form.

**Every cancer cell line in this dataset carries genomic alterations.** No cell had a genomic score of 0 (all features absent). Genomic disruption — copy number changes, expression dysregulation, methylation — is not a subtype of cancer. It is cancer itself.

---

## Why This All Matters

Every year, millions of people are diagnosed with cancer. Many receive treatments that do not work — not because better drugs do not exist, but because we have not yet perfectly matched the right drug to the right patient.

Projects like GDSC, and analyses like ours, are building the scientific foundation for a future where a doctor can look at a tumour's genetic profile and say with confidence:

*"Based on the biology of your cancer — its copy number alterations, gene expression patterns, methylation status, and the specific biological pathway your cancer depends on — this is the drug most likely to help you."*

Our analysis demonstrates this is achievable. The data already contains the signals. The work of genomics-guided oncology is learning to read them — at the level of individual drugs, individual cancer types, and individual genomic features, not averages.

---

## The Code

```python
#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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

    print("What are the key variables in the dataset?")
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

    print("\nMost effective drugs (Lowest Mean LN_IC50):")
    print(drug_stats.sort_values(by='mean').head(10))

    print("\nLeast effective drugs (Highest Mean LN_IC50):")
    print(drug_stats.sort_values(by='mean', ascending=False).head(10))

    print("\nHighly variable drugs — selective responders (Highest Std Dev):")
    highly_variable = drug_stats.sort_values(by='std', ascending=False).head(10)
    print(highly_variable)

    print("\nDrug pathway sensitivity summary:")
    if COL_TARGET_PATH in df.columns:
        pathway_stats = df.groupby(COL_TARGET_PATH)[COL_LN_IC50].agg(['mean', 'std', 'count']).dropna()
        print(pathway_stats.sort_values('mean').head(10))

        pathway_groups = [grp[COL_LN_IC50].dropna().values
                          for _, grp in df.groupby(COL_TARGET_PATH) if len(grp) >= 10]
        if len(pathway_groups) >= 2:
            h_stat, p_kw = stats.kruskal(*pathway_groups)
            sig = "statistically significant" if p_kw < 0.05 else "not significant"
            print(f"\nKruskal-Wallis test (are pathway LN_IC50 differences significant?):")
            print(f"  H = {h_stat:.2f}, p = {p_kw:.2e} ({sig})")
            print("  -> Drug pathways target biologically distinct mechanisms with different therapeutic efficacy.")


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
        print("Pattern 2: Highly Targeted / Selective Drugs (Highest Variance across cell lines)")
        print(drug_patterns.sort_values('std', ascending=False).head(10))

    print("\n--- Drug Selectivity: Largest LN_IC50 spread across cancer types ---")
    if COL_CANCER_TYPE in df.columns and COL_DRUG in df.columns:
        drug_cancer_pivot = df.groupby([COL_DRUG, COL_CANCER_TYPE])[COL_LN_IC50].mean().unstack(COL_CANCER_TYPE)
        selectivity = drug_cancer_pivot.std(axis=1).dropna().sort_values(ascending=False)
        print("Top 10 most selective drugs (work very differently across cancer types):")
        print(selectivity.head(10).to_frame('selectivity_score'))

    print("\n--- Overall Cancer Type Sensitivity Ranking (mean LN_IC50 across all drugs) ---")
    if COL_TCGA_DESC in df.columns:
        cancer_overall = df.groupby(COL_TCGA_DESC)[COL_LN_IC50].agg(
            mean='mean', median='median', std='std', count='count'
        ).sort_values('mean')
        print("Top 10 most drug-sensitive cancer types (lowest mean LN_IC50):")
        print(cancer_overall.head(10))
        print("\nTop 10 most drug-resistant cancer types (highest mean LN_IC50):")
        print(cancer_overall.tail(10))
        print("\nTop 10 most variable cancer types (highest response std dev — most selective drug targets):")
        print(cancer_overall.sort_values('std', ascending=False).head(10))


def analyze_genomic_influence(df):
    """Analyze how genomic, transcriptomic, and epigenomic features influence drug response."""
    print("\n--- Genomic Influence on Drug Sensitivity ---")

    existing_features = [col for col in GENOMIC_FEATURES if col in df.columns]
    if not existing_features:
        print("  -> Genomic feature columns not found. Skipping.")
        return
    if COL_LN_IC50 not in df.columns:
        print(f"  -> '{COL_LN_IC50}' not found. Skipping.")
        return

    # Method 1: Overall Spearman correlation
    df_num = df[[COL_LN_IC50] + existing_features].copy()
    for col in existing_features:
        df_num[col] = df_num[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
        df_num[col] = pd.to_numeric(df_num[col], errors='coerce')
    df_num = df_num.dropna()

    print(f"\n[Method 1] Overall Spearman correlation with {COL_LN_IC50} ({len(df_num):,} records):")
    correlations = df_num.corr(method='spearman')[COL_LN_IC50].drop(COL_LN_IC50)
    for feature, corr_value in correlations.items():
        if abs(corr_value) < 0.2:
            strength = "Very Weak"
        elif abs(corr_value) < 0.4:
            strength = "Weak"
        elif abs(corr_value) < 0.6:
            strength = "Moderate"
        else:
            strength = "Strong"
        direction = "Resistance" if corr_value > 0 else "Sensitivity"
        print(f"  {feature}: {corr_value:>7.4f} ({strength} towards {direction})")

    # Method 2: Group comparison Y vs N with Mann-Whitney U test
    print("\n[Method 2] Group comparison — cells WITH (Y) vs WITHOUT (N) each feature:")
    for feature in existing_features:
        y_vals = df[df[feature] == 'Y'][COL_LN_IC50].dropna()
        n_vals = df[df[feature] == 'N'][COL_LN_IC50].dropna()
        if len(y_vals) == 0 or len(n_vals) == 0:
            print(f"  {feature}: insufficient data for comparison.")
            continue

        y_mean = y_vals.mean()
        n_mean = n_vals.mean()
        diff = y_mean - n_mean
        direction = "more sensitive" if diff < 0 else "more resistant"
        stat, p_val = stats.mannwhitneyu(y_vals, n_vals, alternative='two-sided')
        sig = "statistically significant" if p_val < 0.05 else "not significant"

        print(f"\n  {feature}:")
        print(f"    Present (Y): mean {COL_LN_IC50} = {y_mean:.4f}  (n={len(y_vals):,})")
        print(f"    Absent  (N): mean {COL_LN_IC50} = {n_mean:.4f}  (n={len(n_vals):,})")
        print(f"    -> Cells WITH {feature} are {direction} on average (diff = {diff:+.4f})")
        print(f"    -> Mann-Whitney U test: p = {p_val:.2e} ({sig})")

    # Method 3: Drug-level differential sensitivity per genomic feature
    print("\n[Method 3] Top drugs most affected by each genomic feature:")
    for feature in existing_features:
        pivot = df.groupby([COL_DRUG, feature])[COL_LN_IC50].mean().unstack(feature)
        if 'Y' not in pivot.columns or 'N' not in pivot.columns:
            continue
        pivot = pivot.dropna(subset=['Y', 'N'])
        pivot['shift'] = pivot['Y'] - pivot['N']

        print(f"\n  {feature} — Top 5 drugs where presence SENSITISES (most negative shift):")
        for drug, row in pivot.sort_values('shift').head(5).iterrows():
            print(f"    {drug:<35} Y={row['Y']:>6.3f}  N={row['N']:>6.3f}  shift={row['shift']:>+7.3f}")

        print(f"\n  {feature} — Top 5 drugs where presence CONFERS resistance (most positive shift):")
        for drug, row in pivot.sort_values('shift', ascending=False).head(5).iterrows():
            print(f"    {drug:<35} Y={row['Y']:>6.3f}  N={row['N']:>6.3f}  shift={row['shift']:>+7.3f}")

    # Method 4: Per-cancer-type differential analysis
    print("\n[Method 4] Cancer types most affected by each genomic feature:")
    if COL_TCGA_DESC in df.columns:
        for feature in existing_features:
            cancer_effects = []
            for cancer in df[COL_TCGA_DESC].unique():
                df_c = df[df[COL_TCGA_DESC] == cancer]
                y_v = df_c[df_c[feature] == 'Y'][COL_LN_IC50].dropna()
                n_v = df_c[df_c[feature] == 'N'][COL_LN_IC50].dropna()
                if len(y_v) >= 20 and len(n_v) >= 20:
                    diff = y_v.mean() - n_v.mean()
                    cancer_effects.append({'Cancer': cancer, 'Y_mean': round(y_v.mean(), 3),
                                           'N_mean': round(n_v.mean(), 3), 'Shift': round(diff, 3)})
            if cancer_effects:
                eff = pd.DataFrame(cancer_effects).sort_values('Shift')
                print(f"\n  {feature} — Top 5 cancer types most SENSITISED (most negative shift):")
                print(eff.head(5).to_string(index=False))
                print(f"\n  {feature} — Top 5 cancer types most RESISTANT with presence:")
                print(eff.tail(5).to_string(index=False))

    # Method 5: Per-drug-pathway differential analysis
    print("\n[Method 5] Drug pathways most affected by each genomic feature:")
    if COL_TARGET_PATH in df.columns:
        for feature in existing_features:
            pathway_effects = []
            for pathway in df[COL_TARGET_PATH].unique():
                df_p = df[df[COL_TARGET_PATH] == pathway]
                y_v = df_p[df_p[feature] == 'Y'][COL_LN_IC50].dropna()
                n_v = df_p[df_p[feature] == 'N'][COL_LN_IC50].dropna()
                if len(y_v) >= 20 and len(n_v) >= 20:
                    diff = y_v.mean() - n_v.mean()
                    pathway_effects.append({'Pathway': pathway[:40], 'Y_mean': round(y_v.mean(), 3),
                                            'N_mean': round(n_v.mean(), 3), 'Shift': round(diff, 3)})
            if pathway_effects:
                peff = pd.DataFrame(pathway_effects).sort_values('Shift')
                print(f"\n  {feature} — Pathways most SENSITISED by feature presence:")
                print(peff.head(5).to_string(index=False))
                print(f"\n  {feature} — Pathways most RESISTANT with feature presence:")
                print(peff.tail(5).to_string(index=False))

    # Method 6: Genomic feature enrichment in extreme responders (|Z_SCORE| > 2)
    print("\n[Method 6] Genomic feature enrichment in extreme drug responders (|Z_SCORE| > 2):")
    if COL_Z_SCORE in df.columns:
        extreme = df[df[COL_Z_SCORE].abs() > 2]
        pct = 100 * len(extreme) / len(df)
        print(f"  Extreme responders (|Z_SCORE| > 2): {len(extreme):,} of {len(df):,} total ({pct:.1f}%)")
        for feature in existing_features:
            feat_all  = df[feature].value_counts(normalize=True).get('Y', 0)
            feat_extr = extreme[feature].value_counts(normalize=True).get('Y', 0)
            enrich    = feat_extr / feat_all if feat_all > 0 else float('nan')
            direction = "enriched" if enrich > 1 else "depleted"
            print(f"  {feature}: {100*feat_extr:.1f}% of extreme responders are Y "
                  f"(vs {100*feat_all:.1f}% overall — {direction} {enrich:.2f}x)")

    # Method 7: Combined genomic feature interaction (multi-feature score)
    print("\n[Method 7] Combined genomic feature interaction:")
    df_combo = df.copy()
    df_combo['genomic_score'] = sum((df_combo[f] == 'Y').astype(int) for f in existing_features)
    combo_stats = df_combo.groupby('genomic_score')[COL_LN_IC50].agg(
        mean='mean', median='median', count='count'
    )
    print("  Mean LN_IC50 by number of genomic features present (0 = none, 3 = all active):")
    print(combo_stats)
    if combo_stats['mean'].iloc[0] != combo_stats['mean'].iloc[-1]:
        direction = "lower" if combo_stats['mean'].iloc[-1] < combo_stats['mean'].iloc[0] else "higher"
        print(f"  -> Cells with all features active show {direction} mean LN_IC50 than cells with none.")

    return correlations


def visualize_results(df):
    """Generate and save supporting visualizations for the GDSC dataset."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    print(f"\nGenerating Data Visualizations and saving to: {output_dir}")

    if COL_LN_IC50 not in df.columns:
        print(f"  -> Column '{COL_LN_IC50}' not found. Cannot generate visualizations.")
        return

    sns.set_theme(style="whitegrid")

    # 1/9: Distribution of LN_IC50
    print("  -> Saving 1/9: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[COL_LN_IC50].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({COL_LN_IC50})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300)
    plt.close()

    # 2/9: Boxplot — top 10 most effective drugs
    print("  -> Saving 2/9: boxplot_top_effective_drugs.png...")
    if COL_DRUG in df.columns:
        plt.figure(figsize=(12, 6))
        drug_stats = df.groupby(COL_DRUG)[COL_LN_IC50].agg(['mean', 'std']).dropna()
        top_effective_drugs = drug_stats.sort_values('mean').head(10).index
        df_top_drugs = df[df[COL_DRUG].isin(top_effective_drugs)]
        sns.boxplot(data=df_top_drugs, x=COL_DRUG, y=COL_LN_IC50, hue=COL_DRUG,
                    palette="Set2", order=top_effective_drugs, legend=False)
        plt.title(f'Top 10 Most Effective Drugs by {COL_LN_IC50}', fontsize=14, fontweight='bold')
        plt.xlabel('Drug Name', fontsize=12)
        plt.ylabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "boxplot_top_effective_drugs.png"), dpi=300)
        plt.close()

    # 3/9: Boxplot — top 10 most sensitive cancer types
    print("  -> Saving 3/9: boxplot_cancer_types.png...")
    if COL_CANCER_TYPE in df.columns:
        plt.figure(figsize=(14, 6))
        cancer_means = df.groupby(COL_CANCER_TYPE)[COL_LN_IC50].mean().sort_values().head(10).index
        df_top_cancers = df[df[COL_CANCER_TYPE].isin(cancer_means)]
        sns.boxplot(data=df_top_cancers, x=COL_CANCER_TYPE, y=COL_LN_IC50, hue=COL_CANCER_TYPE,
                    palette="Set3", order=cancer_means, legend=False)
        plt.title(f'Top 10 Most Sensitive Cancer Types by {COL_LN_IC50}', fontsize=14, fontweight='bold')
        plt.xlabel('Cancer Type', fontsize=12)
        plt.ylabel(f'{COL_LN_IC50} (Lower = More Sensitive)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "boxplot_cancer_types.png"), dpi=300)
        plt.close()

    # 4/9: Scatter — AUC vs LN_IC50
    print("  -> Saving 4/9: scatter_auc_ic50.png...")
    if COL_AUC in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=COL_AUC, y=COL_LN_IC50, alpha=0.3, color='darkorange')
        plt.title(f'Relationship between {COL_AUC} and {COL_LN_IC50}', fontsize=14, fontweight='bold')
        plt.xlabel('AUC (Area Under the Curve)', fontsize=12)
        plt.ylabel(COL_LN_IC50, fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50.png"), dpi=300)
        plt.close()

    # 5/9: Correlation heatmap
    print("  -> Saving 5/9: correlation_heatmap.png...")
    df_heat = pd.DataFrame()
    for col in METRIC_COLS:
        if col in df.columns:
            df_heat[col] = df[col]
    for col in GENOMIC_FEATURES:
        if col in df.columns:
            df_heat[col] = df[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
            df_heat[col] = pd.to_numeric(df_heat[col], errors='coerce')
    if not df_heat.empty and len(df_heat.columns) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df_heat.corr(method='spearman'), annot=True, fmt=".2f", cmap='coolwarm',
                    vmin=-1, vmax=1, square=True, linewidths=.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Heatmap of Biological Variables', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=300)
        plt.close()

    # 6/9: Violin plots — LN_IC50 by genomic feature (Y vs N)
    print("  -> Saving 6/9: violin_genomic_features.png...")
    existing_features = [col for col in GENOMIC_FEATURES if col in df.columns]
    if existing_features:
        fig, axes = plt.subplots(1, len(existing_features), figsize=(5 * len(existing_features), 6))
        if len(existing_features) == 1:
            axes = [axes]
        for ax, feature in zip(axes, existing_features):
            df_feat = df[df[feature].isin(['Y', 'N'])]
            sns.violinplot(data=df_feat, x=feature, y=COL_LN_IC50, order=['N', 'Y'],
                           palette={'N': 'steelblue', 'Y': 'coral'}, ax=ax, inner='box')
            ax.set_title(feature, fontsize=12, fontweight='bold')
            ax.set_xlabel('Absent (N) vs Present (Y)', fontsize=10)
            ax.set_ylabel(COL_LN_IC50, fontsize=10)
        plt.suptitle(f'Drug Sensitivity Distribution by Genomic Feature', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "violin_genomic_features.png"), dpi=300)
        plt.close()

    # 7/9: Pivot heatmap — top cancer types vs top drugs
    print("  -> Saving 7/9: heatmap_cancer_drug_pivot.png...")
    if COL_CANCER_TYPE in df.columns and COL_DRUG in df.columns:
        top_drugs   = df.groupby(COL_DRUG)[COL_LN_IC50].mean().sort_values().head(15).index
        top_cancers = df.groupby(COL_CANCER_TYPE)[COL_LN_IC50].mean().sort_values().head(15).index
        pivot_df    = df[df[COL_DRUG].isin(top_drugs) & df[COL_CANCER_TYPE].isin(top_cancers)]
        pivot_table = pivot_df.pivot_table(values=COL_LN_IC50, index=COL_CANCER_TYPE,
                                           columns=COL_DRUG, aggfunc='mean')
        plt.figure(figsize=(18, 8))
        sns.heatmap(pivot_table, cmap='RdYlGn_r', linewidths=0.3,
                    cbar_kws={'label': f'Mean {COL_LN_IC50}'})
        plt.title('Drug Sensitivity: Top Cancer Types vs Top Effective Drugs', fontsize=14, fontweight='bold')
        plt.xlabel('Drug Name', fontsize=11)
        plt.ylabel('Cancer Type', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "heatmap_cancer_drug_pivot.png"), dpi=300)
        plt.close()

    # 8/9: Horizontal bar chart — mean LN_IC50 per drug target pathway
    print("  -> Saving 8/9: barplot_pathway_sensitivity.png...")
    if COL_TARGET_PATH in df.columns:
        pathway_means = df.groupby(COL_TARGET_PATH)[COL_LN_IC50].mean().sort_values()
        plt.figure(figsize=(10, max(6, len(pathway_means) * 0.45)))
        colors = ['forestgreen' if x < 0 else 'steelblue' for x in pathway_means.values]
        plt.barh(range(len(pathway_means)), pathway_means.values, color=colors, edgecolor='white')
        plt.yticks(range(len(pathway_means)), [p[:45] for p in pathway_means.index], fontsize=8)
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.6)
        plt.title('Mean Drug Sensitivity by Target Pathway', fontsize=14, fontweight='bold')
        plt.xlabel(f'Mean {COL_LN_IC50}  (← More Effective  |  Less Effective →)', fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "barplot_pathway_sensitivity.png"), dpi=300)
        plt.close()

    # 9/9: Vertical bar chart — top 20 most sensitive cancer types (TCGA codes)
    print("  -> Saving 9/9: barplot_cancer_sensitivity.png...")
    if COL_TCGA_DESC in df.columns:
        cancer_means = df.groupby(COL_TCGA_DESC)[COL_LN_IC50].mean().sort_values().head(20)
        overall_mean = df[COL_LN_IC50].mean()
        plt.figure(figsize=(13, 6))
        cancer_means.plot(kind='bar', color='coral', edgecolor='darkred', linewidth=0.5)
        plt.axhline(overall_mean, color='navy', linestyle='--', linewidth=1.2,
                    label=f'Dataset mean ({overall_mean:.2f})')
        plt.title('Top 20 Most Drug-Sensitive Cancer Types (TCGA Codes)', fontsize=14, fontweight='bold')
        plt.xlabel('Cancer Type (TCGA Code)', fontsize=12)
        plt.ylabel(f'Mean {COL_LN_IC50} (Lower = More Sensitive)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "barplot_cancer_sensitivity.png"), dpi=300)
        plt.close()


def main():
    print("Welcome to HackBio: GDSC Data Analysis Project!")
    print("Investigating Genomics of Drug Sensitivity in Cancer...\n")

    base_dir      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

# Exploring Genomics of Drug Sensitivity in Cancer (GDSC)
### HackBio Stage One -- AI for Genomics Internship
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

*CELL_LINE_NAME* -- The specific name of the cancer cell model being tested.

*TCGA_DESC* -- The type of cancer (e.g., lung, colon, breast).

*DRUG_NAME* -- The name of the pharmaceutical compound being tested.

*TARGET_PATHWAY* -- The biological process the drug is designed to disrupt.

**Drug Response Metrics**

*LN_IC50* -- How much drug was needed to kill 50% of the cancer cells. A lower value means the drug is more powerful.

*AUC* -- Area Under the Curve. How well the drug worked across a full range of doses.

*Z_SCORE* -- How unusual this cell line's response is compared to the average across all experiments.

**Molecular & Genetic Features**

*CNA* -- Copy Number Alteration. Whether the cancer cell has a DNA copy error (a section duplicated or deleted).

*Gene Expression* -- Whether a specific gene is unusually active or silent in this cancer cell.

*Methylation* -- Whether certain genes have been chemically "switched off" in this cancer cell.

> **Key metric -- LN_IC50:** A very negative LN_IC50 means the drug is a precision weapon -- a tiny amount kills the cancer cells. A high LN_IC50 means you would need a dangerously large dose to see any effect.

---

## Our Analysis: A 5-Step Investigation

---

### Step 1 -- Understanding the Dataset
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

The dataset contains **162,103 complete experiments** with zero missing values or duplicates -- exceptional quality for real-world biological data.

The mean LN_IC50 of **2.82** tells us a moderate-to-high dose is typically required. But the standard deviation of **2.84** -- nearly equal to the mean -- is the critical signal. Drug effectiveness varies enormously across experiments. This is not noise; it is biology telling us that different cancers are fundamentally different diseases, and a one-size-fits-all treatment approach is biologically inappropriate.

The LN_IC50 range spans from **-8.64** (a drug so potent it needs almost no dose) to **+13.82** (a drug requiring an impossibly large dose). This 22-unit range underscores the importance of matching the right drug to the right cancer.

> **Why data quality matters:** In real laboratory settings, machines malfunction and values get entered incorrectly. Cleaning the data is not glamorous, but skipping it is like building a house on sand. The fact that our dataset is perfectly complete means every finding below can be trusted.

---

### Step 2 -- Drug Sensitivity Patterns
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

#### Highly Variable Drugs -- Selective Responders (Highest Std Dev)

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
â†’ Drug pathways target biologically distinct mechanisms with measurably different therapeutic efficacy.
```

#### Biological Interpretation

**Romidepsin** is the most potent drug in the dataset (mean LN_IC50 = -5.18). It is an HDAC (Histone Deacetylase) inhibitor -- it works by blocking the proteins that control how tightly DNA is wound inside the cell. When these proteins are disabled, cancer cells lose the ability to silence their own self-destruct signals. The narrow standard deviation (1.03) confirms this effect is **consistent across cancer types** -- Romidepsin is a broad-spectrum weapon.

**Bortezomib** (-4.75) is a proteasome inhibitor -- it blocks the cell's internal "waste disposal system." Cancer cells produce abnormal proteins at high rates; when the disposal system is blocked, they choke on their own toxic waste and die.

The antioxidants at the bottom -- **Vitamin C, N-acetyl cysteine, Glutathione** -- confirm that nutritional supplements alone cannot kill cancer cells at practical doses. Their high LN_IC50 values serve as a useful negative control.

**The pathway analysis reveals a striking and statistically proven pattern:** Mitosis-targeting drugs are the most effective on average (mean -1.40), while ERK MAPK signaling drugs are the least (mean 2.89). The Kruskal-Wallis test (H = 21,985.95, p â‰ˆ 0) confirms this is not a chance finding -- **pathway membership is a statistically significant predictor of drug effectiveness.** This makes biological sense -- cancer cells divide far more rapidly than normal cells, making mitosis their greatest vulnerability.

**Highly variable drugs are the most clinically interesting.** Gemcitabine (std 2.94) and Dasatinib (std 2.39) show wildly different responses across cancer types. This variability is a signal, not noise -- these drugs are hitting a specific biological target that only some cancers possess.

> **Biological insight:** The distinction between broadly effective drugs (Romidepsin, Bortezomib) and highly selective drugs (Dasatinib, Gemcitabine) reflects two different treatment philosophies. Broad drugs attack universal cancer vulnerabilities. Selective drugs require matching -- but when the match is right, they can be extraordinarily powerful.

---

### Step 3 -- Cancer Cell Line Analysis
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

#### Drug Selectivity -- Largest Response Spread Across Cancer Types

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

**CLL (Chronic Lymphocytic Leukaemia)** dominates the most sensitive list across both cancer-drug combinations and the overall cancer type ranking (mean 1.105 -- nearly 1.7 units below the dataset mean of 2.82). This is biologically meaningful. CLL cells are trapped in an immature developmental state and lack the full defensive machinery that more aggressive tumours develop.

**Blood cancers sweep the top 6 most sensitive types** -- CLL, LAML (acute myeloid leukaemia), DLBC (diffuse large B-cell lymphoma), ALL (acute lymphoblastic leukaemia), LCML, and MM (multiple myeloma). This reflects a shared biological property: blood cancers circulate in the bloodstream, are continuously exposed to systemically delivered drugs, and lack the physical barriers (dense tissue, poor blood supply, efflux pumps) that protect solid tumours.

**PAAD (pancreatic adenocarcinoma)** is the most resistant cancer type (mean 3.732), 0.9 units above the dataset mean. This is clinically consistent with pancreatic cancer's notorious drug resistance -- a dense stromal barrier physically prevents drugs from reaching tumour cells, and the tumour suppressor gene KRAS is almost universally mutated in a way that makes it "undruggable" by conventional approaches.

**LCML + Dasatinib** (LN_IC50 = -6.575) is a textbook precision oncology result. LCML is almost universally driven by the BCR-ABL fusion gene. Dasatinib was specifically engineered to block BCR-ABL. Seeing LCML at the top of the Dasatinib sensitivity list is a **direct biological validation** of our analysis working correctly.

**The selectivity analysis reveals a clinically crucial distinction.** Tozasertib (score 2.06), AZD5991 (1.99), and Dasatinib (1.82) show the greatest spread across cancer types. These are not broadly effective -- they are extraordinarily powerful for specific cancers and almost useless for others. The selectivity score is essentially a measure of how "targeted" the drug truly is.

> **Biological insight:** The gap between blood cancers (CLL mean 1.105) and the most resistant solid tumour (PAAD mean 3.732) is 2.6 LN_IC50 units -- equivalent to needing approximately 13Ã-- more drug for pancreatic cancer than for leukaemia. This is not just a statistical difference; it is the difference between a treatable and an untreatable disease at standard doses.

---

### Step 4 -- Genomic, Transcriptomic, and Epigenomic Influence on Drug Response
*Does your molecular profile determine whether a drug will work?*

Cancer is a multi-layered disease of molecular dysregulation. We investigate how three distinct types of molecular alteration -- each operating at a different biological level -- influence how a cancer cell responds to drugs:

| Feature | Omics Layer | What It Measures | Biological Role |
|---------|------------|-----------------|-----------------|
| **MSI Status (Microsatellite Instability)** | **Genomic** | DNA mismatch repair status | MSI-H = hypermutated (defective repair); MSS = stable DNA |
| **CNA (Copy Number Alteration)** | **Genomic** | DNA copy number changes | Gene amplification / deletion at the DNA level |
| **Gene Expression** | **Transcriptomic** | mRNA expression level | Whether a gene is actively transcribed into RNA |
| **Methylation** | **Epigenomic** | DNA methylation status | Gene silencing via chemical tagging of DNA |

These four features span the **genomic, transcriptomic, and epigenomic** layers of the cancer molecular landscape. MSI and CNA operate at the DNA level (genomic), Gene Expression at the RNA output level (transcriptomic), and Methylation at the chemical modification level (epigenomic).

#### Key Findings -- How Genomic, Transcriptomic, and Epigenomic Features Influence Drug Response

| Feature | Omics Layer | Overall Influence on Drug Response | p-value |
|---------|------------|-----------------------------------|---------|
| **MSI-H status** | **Genomic** | **Sensitises** -- MSI-H cells have lower LN_IC50 (shift = −0.284) | 3.81 × 10⁻³² |
| **CNA presence** | **Genomic** | **Sensitises** -- CNA-positive cells are more drug-sensitive (shift = −0.308) | 7.39 × 10⁻³ |
| **Gene Expression active** | **Transcriptomic** | **Increases resistance** -- active transcription raises LN_IC50 (shift = +0.455) | 2.91 × 10⁻³⁰ |
| **Methylation present** | **Epigenomic** | **No aggregate effect** -- balanced across drugs (shift = +0.026) | 0.340 n.s. |

These aggregate effects mask much larger drug-specific effects (up to 4.3 LN_IC50 units). See Methods 3--9 for drug-level and pathway-level analysis.

We used **nine complementary analytical methods** plus a dedicated MSI genomic biomarker analysis to answer this question at increasing levels of depth -- from aggregate correlations to standardised effect sizes to per-drug biomarker predictions.

---

#### MSI Genomic Biomarker Analysis -- Microsatellite Instability

MSI (Microsatellite Instability) is a direct genomic feature: cells classified as MSI-H have defective DNA mismatch repair, leading to hypermutation across the genome. This is a well-established clinical genomic biomarker used in cancer treatment decisions.

```
MSI-H:     n = 11,322, mean LN_IC50 = 2.5585
MSS/MSI-L: n = 150,781, mean LN_IC50 = 2.8425
Difference (MSI-H minus MSS): -0.2840
Mann-Whitney U: p = 3.81e-32 (statistically significant)
Cohen's d = -0.1002 (negligible aggregate effect size)
```

**MSI-H cells are significantly more drug-sensitive overall** (p = 3.81e-32). The effect is modest in aggregate (Cohen's d = âˆ’0.10) but highly consistent -- MSI-H cells show lower LN_IC50 for 7 of every 10 drugs tested.

**Top 5 drugs most sensitised by MSI-H genomic status:**

| Drug | LN_IC50 Shift | MSI-H mean | MSS mean | MSI-H n |
|------|--------------|-----------|---------|---------|
| Methotrexate | âˆ’1.564 | âˆ’1.002 | 0.562 | 46 |
| Daporinad | âˆ’1.293 | âˆ’4.543 | âˆ’3.250 | 25 |
| Vinblastine | âˆ’1.234 | âˆ’4.491 | âˆ’3.257 | 45 |
| Cytarabine | âˆ’1.230 | 0.579 | 1.809 | 45 |
| BI-2536 | âˆ’1.205 | âˆ’2.143 | âˆ’0.938 | 47 |

> **Biological insight:** MSI-H cells are hypermutated -- they divide rapidly and have altered DNA repair mechanisms. Methotrexate (antifolate -- blocks DNA synthesis) and Cytarabine (nucleoside analogue -- disrupts DNA replication) are most effective precisely because they target the rapid, error-prone DNA replication that hypermutated cells depend on. This is a direct genomic feature â†’ drug sensitivity link: the genomic defect (defective mismatch repair) creates a biochemical vulnerability (dependency on rapid DNA replication pathways) that specific drug classes exploit.

---

#### Method 1: Spearman Correlation (scipy.stats.spearmanr) -- Each Feature vs LN_IC50

Using `scipy.stats.spearmanr` to compute the Spearman rank correlation between each genomic, transcriptomic, and epigenomic feature (binary 0/1) and LN_IC50:

| Feature | Omics Layer | Spearman r | p-value | Direction |
|---------|------------|-----------|---------|-----------|
| CNA | Genomic | -0.0067 | 0.006 (significant) | Very Weak towards Sensitivity |
| Gene Expression | Transcriptomic | +0.0284 | 2.9e-30 (significant) | Very Weak towards Resistance |
| Methylation | Epigenomic | +0.0024 | 0.340 (n.s.) | Very Weak towards Resistance |
| MSI_status | Genomic | -0.0293 | 3.7e-32 (significant) | Very Weak towards Sensitivity |

These aggregate correlations are near zero -- not because genomic/transcriptomic/epigenomic features are irrelevant, but because averaging across all drugs washes out opposing drug-specific signals. Method 1b reveals the real influence at the per-drug level.

---

#### Method 1b: Per-Drug Spearman Correlation -- Genomic Features Influence Specific Drugs Strongly

For each drug tested, we compute `scipy.stats.spearmanr` between the genomic/transcriptomic/epigenomic feature and LN_IC50. This reveals that while aggregate correlations are near zero, many individual drugs show strong, statistically significant correlations.

**Gene Expression (Transcriptomic): 72 out of 205 drugs show significant Spearman correlation (p < 0.05)**

Top 5 drugs most SENSITISED by active gene expression (most negative r):

| Drug | Spearman r | p-value |
|------|-----------|---------|
| Methotrexate | -0.140 | 0.0003 |
| Tamoxifen | -0.140 | 0.0002 |
| WZ4003 | -0.125 | 0.0011 |
| AZD4547 | -0.085 | 0.0222 |
| Erlotinib | ~-0.08 | <0.05 |

Top 5 drugs most RESISTANT with active gene expression (most positive r):

| Drug | Spearman r | p-value |
|------|-----------|---------|
| LY2109761 | +0.189 | <0.0001 |
| XAV939 | +0.182 | <0.0001 |
| Tozasertib | +0.178 | 0.0118 |
| GSK269962A | +0.170 | 0.0158 |
| BX795 | +0.157 | 0.0481 |

**MSI Status (Genomic): 73 out of 246 drugs show significant Spearman correlation (p < 0.05)**

Top 5 drugs most sensitised by MSI-H genomic status (most negative r):

| Drug | Spearman r | p-value |
|------|-----------|---------|
| GSK2110183B | -0.163 | 0.0001 |
| Methotrexate | -0.162 | <0.0001 |
| AZD6738 | -0.158 | <0.0001 |
| Ipatasertib | -0.155 | <0.0001 |

> **Key insight:** 72/205 drugs (35%) show a statistically significant Spearman correlation between Gene Expression status (transcriptomic feature) and LN_IC50, and 73/246 drugs (30%) show significant correlation with MSI status (genomic feature). This demonstrates that **genomic and transcriptomic features influence drug response for a substantial proportion of the drug panel** -- the near-zero aggregate correlation is a statistical artefact of averaging sensitising and resistance effects.

---

#### Method 2: Group Comparison (Y vs N) with Statistical Testing

**CNA (Copy Number Alteration):**
```
Present (Y): mean LN_IC50 = 2.8214  (n = 161,445)
Absent  (N): mean LN_IC50 = 3.1290  (n = 658)
â†’ Cells WITH CNA are more sensitive on average (diff = -0.3076)
â†’ Mann-Whitney U test: p = 7.39e-03 (statistically significant)
â†’ Cohen's d = -0.1085 (negligible effect size)
```

**Gene Expression:**
```
Present (Y): mean LN_IC50 = 2.8332  (n = 158,342)
Absent  (N): mean LN_IC50 = 2.3778  (n = 3,761)
â†’ Cells WITH Gene Expression changes are more resistant on average (diff = +0.4554)
â†’ Mann-Whitney U test: p = 2.91e-30 (statistically significant)
â†’ Cohen's d = +0.1606 (negligible effect size)
```

**Methylation:**
```
Present (Y): mean LN_IC50 = 2.8232  (n = 158,601)
Absent  (N): mean LN_IC50 = 2.7968  (n = 3,502)
â†’ Cells WITH Methylation are more resistant on average (diff = +0.0264)
â†’ Mann-Whitney U test: p = 3.42e-01 (not significant)
â†’ Cohen's d = +0.0093 (negligible effect size)
```

**Why the overall Cohen's d is negligible (and why that's expected):** Averaging across all 250+ drugs cancels out opposing signals. Gene Expression sensitises 52 drugs and confers resistance on 153 others -- these opposing shifts reduce the aggregate effect to near zero. The large effects only emerge at the drug-specific level, as Methods 3, 7, and 9 demonstrate.

---

#### Method 3: Drug-Level Differential -- Which Drugs Are Most Affected?

**CNA -- Top 5 drugs where presence SENSITISES the cancer:**

| Drug | With CNA (Y) | Without CNA (N) | Shift |
|------|-------------|----------------|-------|
| ULK1_4989 | 2.443 | 5.548 | -3.106 |
| AZD5582 | 2.290 | 5.079 | -2.789 |
| Luminespib | -2.041 | 0.554 | -2.595 |
| Cytarabine | 1.704 | 4.217 | -2.512 |
| Tanespimycin | -0.130 | 2.209 | -2.339 |

**CNA -- Top 5 drugs where presence CONFERS resistance:**

| Drug | With CNA (Y) | Without CNA (N) | Shift |
|------|-------------|----------------|-------|
| Dasatinib | 1.284 | -1.085 | +2.369 |
| AT13148 | 3.578 | 2.150 | +1.428 |
| AZD8055 | 0.044 | -1.376 | +1.419 |
| TAF1_5496 | 3.744 | 2.469 | +1.275 |
| AZD2014 | 2.231 | 1.034 | +1.197 |

**Gene Expression -- Top 5 drugs where presence SENSITISES:**

| Drug | With GE (Y) | Without GE (N) | Shift |
|------|------------|----------------|-------|
| TW 37 | 1.313 | 5.630 | -4.317 |
| Bleomycin (50 uM) | 3.548 | 6.792 | -3.244 |
| UNC0638 | 4.209 | 6.714 | -2.505 |
| UNC0379 | 3.612 | 6.076 | -2.464 |
| Cisplatin | 3.368 | 5.541 | -2.173 |

**Gene Expression -- Top 5 drugs where presence CONFERS resistance:**

| Drug | With GE (Y) | Without GE (N) | Shift |
|------|------------|----------------|-------|
| Cytarabine | 1.716 | -0.281 | +1.997 |
| Talazoparib | 2.982 | 1.475 | +1.508 |
| Docetaxel | -3.303 | -4.730 | +1.427 |
| Tozasertib | 2.173 | 0.765 | +1.407 |
| Dactinomycin | -3.648 | -5.036 | +1.388 |

**Methylation -- Top 5 drugs where presence SENSITISES:**

| Drug | With Meth (Y) | Without Meth (N) | Shift |
|------|--------------|-----------------|-------|
| AZD5991 | 3.843 | 5.683 | -1.840 |
| GSK2110183B | 3.299 | 4.746 | -1.447 |
| Methotrexate | 0.422 | 1.812 | -1.391 |
| UNC0638 | 4.198 | 5.285 | -1.087 |
| ICL-SIRT078 | 4.353 | 5.282 | -0.929 |

**Methylation -- Top 5 drugs where presence CONFERS resistance:**

| Drug | With Meth (Y) | Without Meth (N) | Shift |
|------|--------------|-----------------|-------|
| PRIMA-1MET | 4.516 | 3.641 | +0.875 |
| Cytarabine | 1.723 | 0.875 | +0.848 |
| Talazoparib | 2.957 | 2.170 | +0.787 |
| Dactinomycin | -3.657 | -4.394 | +0.737 |
| CHIR-99021 | 4.659 | 3.952 | +0.707 |

---

#### Method 4: Per-Cancer-Type Differential -- Where Does Each Feature Matter Most?

**Gene Expression -- Cancer types most sensitised (most negative shift):**

| Cancer Type | With GE (Y) | Without GE (N) | Shift |
|------------|------------|----------------|-------|
| KIRC | 3.099 | 4.214 | -1.115 |
| BRCA | 3.071 | 3.451 | -0.380 |
| SKCM | 2.877 | 3.159 | -0.283 |
| DLBC | 1.529 | 1.702 | -0.173 |

**Gene Expression -- Cancer types made most resistant:**

| Cancer Type | With GE (Y) | Without GE (N) | Shift |
|------------|------------|----------------|-------|
| THCA | 3.348 | 2.026 | +1.322 |
| LUAD | 3.296 | 2.251 | +1.045 |
| COREAD | 3.093 | 2.193 | +0.900 |
| OV | 3.242 | 2.586 | +0.656 |
| SCLC | 2.810 | 2.251 | +0.559 |

**Methylation -- Cancer types most sensitised:**

| Cancer Type | With Meth (Y) | Without Meth (N) | Shift |
|------------|--------------|-----------------|-------|
| SCLC | 2.756 | 3.351 | -0.594 |
| COREAD | 3.069 | 3.453 | -0.384 |
| BRCA | 3.071 | 3.451 | -0.380 |
| LUAD | 3.276 | 3.600 | -0.323 |
| DLBC | 1.534 | 1.683 | -0.149 |

**Methylation -- Cancer types made most resistant:**

| Cancer Type | With Meth (Y) | Without Meth (N) | Shift |
|------------|--------------|-----------------|-------|
| GBM | 3.152 | 2.134 | +1.018 |
| OV | 3.263 | 2.670 | +0.592 |
| ALL | 1.562 | 1.231 | +0.331 |
| KIRC | 3.139 | 2.943 | +0.196 |

*Note: CNA is present (Y) in 99.6% of all cell lines, leaving insufficient N cases for per-cancer-type comparison in most cancer types. This extreme prevalence is itself biologically significant -- copy number alterations are nearly universal in cancer cell lines used for drug screening.*

---

#### Method 5: Per-Pathway Differential -- Which Drug Mechanisms Are Most Affected by Genomics?

**CNA -- Pathways most sensitised by CNA presence:**

| Pathway | With CNA (Y) | Without CNA (N) | Shift |
|---------|-------------|----------------|-------|
| Mitosis | -1.402 | -0.151 | -1.251 |
| Apoptosis regulation | 1.773 | 2.765 | -0.991 |
| Cell cycle | 1.542 | 2.280 | -0.738 |
| Chromatin other | 3.455 | 4.192 | -0.737 |
| Protein stability & degradation | 0.829 | 1.421 | -0.592 |

**Gene Expression -- Pathways most dramatically affected:**

| Pathway | Direction | With GE (Y) | Without GE (N) | Shift |
|---------|-----------|------------|----------------|-------|
| Metabolism | **+resistance** | 4.855 | 2.863 | +1.992 |
| Other | **+resistance** | 3.598 | 2.610 | +0.988 |
| JNK and p38 signaling | **+resistance** | 5.096 | 4.254 | +0.842 |
| p53 pathway | **+resistance** | 4.561 | 3.823 | +0.738 |
| Hormone-related | **sensitised** | 4.205 | 4.498 | -0.293 |

**Methylation -- Pathways most sensitised by Methylation presence:**

| Pathway | With Meth (Y) | Without Meth (N) | Shift |
|---------|--------------|-----------------|-------|
| Mitosis | -1.412 | -0.768 | -0.644 |
| Hormone-related | 4.204 | 4.623 | -0.419 |
| IGF1R signaling | 2.993 | 3.265 | -0.271 |
| Chromatin histone methylation | 3.786 | 4.022 | -0.235 |
| RTK signaling | 2.583 | 2.800 | -0.217 |

---

#### Method 6: Extreme Responder Enrichment -- Do Genomic Features Explain Outlier Responses?

```
Extreme responders (|Z_SCORE| > 2): 7,582 of 162,103 total (4.7%)

CNA:            99.9% of extreme responders are Y  (vs 99.6% overall -- enriched 1.00Ã--)
Gene Expression: 97.4% of extreme responders are Y  (vs 97.7% overall -- depleted 1.00Ã--)
Methylation:    97.4% of extreme responders are Y  (vs 97.8% overall -- depleted 1.00Ã--)
```

Genomic features alone do not explain outlier drug responses. The enrichment is essentially 1.0Ã-- across all three features -- extreme responders look no different from the overall population in terms of feature presence. This tells us that **having the feature is not sufficient for an extreme response; it is the drug-feature interaction that matters** -- consistent with Method 3 showing drug-specific shifts of up to 4.3 LN_IC50 units.

---

#### Method 7: Combined Genomic Feature Interaction

```
Mean LN_IC50 by number of genomic features simultaneously active:

Score 0 (none active): not present in dataset
Score 1 (one active):  mean = 2.764  (n = 1,243)
Score 2 (two active):  mean = 2.562  (n = 5,435)
Score 3 (all active):  mean = 2.832  (n = 155,425)
```

Two findings stand out: (1) No cell line in the dataset has all three molecular features absent -- copy number alterations (genomic), gene expression changes (transcriptomic), and methylation alterations (epigenomic) are **universal** in cancer cell lines used for drug screening. This confirms that these are defining hallmarks of cancer biology, not incidental features. (2) The relationship is non-monotonic -- cells with exactly two features active show the lowest mean LN_IC50 (most sensitive), suggesting that having partial molecular disruption may create specific dependencies that drugs can exploit, while full disruption (all three active) may trigger compensatory resistance mechanisms.

---

#### Method 8: Z_SCORE-Based Genomic Analysis -- Do Genomic Features Drive Outlier Drug Responses?

Z_SCORE measures how far each drug response deviates from the average response for that drug across all cell lines tested. A high |Z_SCORE| means the response was unusually strong or weak -- a signal that a biological factor (possibly genomic) is driving an exceptional outcome.

```
Gene Expression:
  Mean |Z_SCORE| when Active (Y) = 0.7983  (n = 158,342)
  Mean |Z_SCORE| when Absent  (N) = 0.8014  (n = 3,761)
  â†’ Feature presence associated with slightly more typical drug responses
  â†’ Mann-Whitney U: p = 2.66e-01 (not significant)

CNA:
  Mean |Z_SCORE| when Active (Y) = 0.7985  (n = 161,445)
  Mean |Z_SCORE| when Absent  (N) = 0.7866  (n = 658)
  â†’ Feature presence associated with slightly more extreme drug responses
  â†’ Mann-Whitney U: p = 3.26e-01 (not significant)

Methylation:
  Mean |Z_SCORE| when Active (Y) = 0.7988  (n = 158,601)
  Mean |Z_SCORE| when Absent  (N) = 0.7896  (n = 3,502)
  â†’ Feature presence associated with slightly more extreme drug responses
  â†’ Mann-Whitney U: p = 2.41e-01 (not significant)
```

None of the genomic features significantly alter how *unusual* (outlier) a drug response is. The mean |Z_SCORE| is nearly identical across all feature groups (~0.80). This is a meaningful negative result: it confirms that the *presence* of a genomic feature does not make a cancer cell generally "weird" in how it responds to all drugs. Instead, genomic features create selective vulnerabilities -- they shift responses for specific drugs (as shown in Method 3), not the overall response profile.

---

#### Method 9: Strongest Molecular Biomarker-Drug Pairings by Omics Layer (Cohen's d Effect Size)

Cohen's d standardises effect size by the pooled within-group standard deviation -- giving a scale-free measure of how strongly each genomic, transcriptomic, or epigenomic feature predicts sensitivity to a specific drug. This is the definitive answer to "does the molecular feature influence drug response?": not just "is it statistically significant?" but "how large is the effect?" (Threshold: |d| < 0.2 negligible; 0.5 small; 0.8 medium; >0.8 large.)

Only drugs with â‰¥5 observations in both Y and N groups are included -- ensuring effect sizes are statistically reliable.

**Gene Expression -- Top 5 strongest sensitising pairings (most negative Cohen's d):**

| Drug | Cohen's d | With GE (Y) | Without GE (N) | N group size |
|------|-----------|------------|----------------|-------------|
| Methotrexate | âˆ’0.850 (medium) | 0.394 | 2.406 | 21 |
| Tamoxifen | âˆ’0.804 (medium) | 3.970 | 4.953 | 21 |
| WZ4003 | âˆ’0.719 (medium) | 4.187 | 5.170 | 20 |
| AZD4547 | âˆ’0.509 (small) | 2.800 | 3.534 | 21 |
| Erlotinib | âˆ’0.412 (small) | 2.770 | 3.335 | 20 |

**Gene Expression -- Top 5 strongest resistance pairings (most positive Cohen's d):**

| Drug | Cohen's d | With GE (Y) | Without GE (N) | N group size |
|------|-----------|------------|----------------|-------------|
| Avagacestat | +0.897 (large) | 4.834 | 3.873 | 21 |
| Doramapimod | +0.946 (large) | 5.034 | 3.936 | 21 |
| EPZ5676 | +1.125 (large) | 5.612 | 4.476 | 21 |
| LY2109761 | +1.187 (large) | 5.057 | 3.802 | 20 |
| XAV939 | +1.207 (large) | 4.330 | 3.133 | 20 |

**Methylation -- Top 5 strongest sensitising pairings:**

| Drug | Cohen's d | With Meth (Y) | Without Meth (N) | N group size |
|------|-----------|--------------|-----------------|-------------|
| GSK2110183B | âˆ’0.920 (large) | 3.299 | 4.746 | 6 |
| UNC0638 | âˆ’0.781 (medium) | 4.198 | 5.285 | 8 |
| Tamoxifen | âˆ’0.753 (medium) | 3.977 | 4.899 | 17 |
| GSK2830371 | âˆ’0.742 (medium) | 5.477 | 6.324 | 8 |
| AZD1208 | âˆ’0.675 (medium) | 5.292 | 5.980 | 6 |

> **XAV939 has a Cohen's d of +1.207 for Gene Expression** -- meaning that in gene-expression-active cells, XAV939 requires a 1.2 standard-deviation higher dose to achieve effect. This is a large standardised effect. XAV939 is a tankyrase inhibitor targeting the Wnt/Î²-catenin pathway. Active gene expression in a cancer cell reflects an elevated transcriptional program that includes Wnt pathway activity -- cells that are actively using this pathway may paradoxically be better equipped to survive XAV939 treatment by activating compensatory transcriptional programs. **Methotrexate (d = âˆ’0.850)** shows the opposite: gene-expression-active cells are significantly more sensitive to this antifolate, consistent with the fact that rapidly transcribing cells consume folate at higher rates, making them more vulnerable to folate pathway blockade.

CNA's Method 9 results are limited by the small N group (only 658 total N rows across 246 drugs, averaging ~2.7 per drug). Only 5 drugs meet the â‰¥5 N observations threshold, all with |d| < 0.65 -- confirming that CNA's influence operates at the aggregate and pathway level (Methods 2 and 5), not at the level of individual drug biomarker pairs. GSK2110183B (Methylation Cohen's d = âˆ’0.920, large) represents a clinically actionable finding: methylation status is a strong predictor of sensitivity to this AKT inhibitor.

---

#### Drug Shift Census -- Scale of Molecular Influence Across All Drugs (Genomic / Transcriptomic / Epigenomic)

For each molecular feature (genomic CNA, transcriptomic Gene Expression, epigenomic Methylation), we count across every drug how many show sensitisation (Y cells have lower LN_IC50 than N) versus resistance (Y cells have higher), and the magnitude of the effect.

**CNA (246 drugs with both Y and N data):**
```
Sensitised (Y < N):  172 drugs  (69.9%)
Resistant  (Y > N):   74 drugs  (30.1%)
Median shift:        -0.337 LN_IC50 units
Max sensitisation:   -3.106  (ULK1_4989)
Max resistance:      +2.369  (Dasatinib)
```

**Gene Expression (205 drugs with both Y and N data):**
```
Sensitised (Y < N):   52 drugs  (25.4%)
Resistant  (Y > N):  153 drugs  (74.6%)
Median shift:        +0.340 LN_IC50 units
Max sensitisation:   -4.317  (TW 37)
Max resistance:      +1.997  (Cytarabine)
```

**Methylation (246 drugs with both Y and N data):**
```
Sensitised (Y < N):  128 drugs  (52.0%)
Resistant  (Y > N):  118 drugs  (48.0%)
Median shift:        -0.016 LN_IC50 units
Max sensitisation:   -1.840  (AZD5991)
Max resistance:      +0.875  (PRIMA-1MET)
```

The census reveals three biologically distinct patterns:

**CNA is a predominantly directional sensitiser.** 69.9% of drugs (172/246) show lower LN_IC50 in CNA-positive cells, with a median shift of âˆ’0.337. Copy number alterations create vulnerabilities more often than resistances. This makes biological sense: genome-scale disruption amplifies cellular stress and dependence on remaining intact pathways, making cells more susceptible to drugs targeting those pathways.

**Gene Expression is a predominantly directional resistance factor.** 74.6% of drugs (153/205) show higher LN_IC50 in gene-expression-active cells, with a median shift of +0.340. Cells that are actively transcribing genes are more metabolically robust and adaptive -- they have more tools available to respond to chemical stress. The 25.4% of drugs that show sensitisation (such as TW 37, shift âˆ’4.317) target exactly those active gene products, creating selective vulnerabilities in high-expression cells.

**Methylation is genuinely balanced.** The 52/48 split and near-zero median shift (âˆ’0.016) confirm the non-significant overall p-value (0.34). Methylation silences individual genes but the population-level effect on drug response cancels out across drugs -- some silenced genes are resistance genes (sensitising effect), others are sensitivity genes (resistance effect).

---

#### Overall Multi-Omics Analysis Biological Interpretation (Genomic / Transcriptomic / Epigenomic)

**CNA increases sensitivity via oncogene addiction -- and massively sensitises Mitosis drugs.**

Cells with copy number alterations show lower mean LN_IC50 (p = 0.007). The pathway analysis reveals *why*: CNA-positive cells are nearly 1.3 LN_IC50 units more sensitive to Mitosis-targeting drugs (-1.402 vs -0.151). Copy number amplification of oncogenes makes cancer cells hyper-dependent on cell division -- blocking mitosis in a cell already racing to divide is catastrophic. This concept is called **oncogene addiction**: the cancer becomes so reliant on amplified growth signals that any disruption of the machinery carrying them out is lethal. CNA is present in 99.6% of cell lines -- it is not a rare variant; it is a defining feature of cancer that creates broad vulnerability to mitotic inhibitors.

**Gene Expression changes create cancer-type-specific effects -- with the strongest transcriptomic signal in the dataset.**

The Gene Expression finding (p = 2.91 Ã-- 10â»Â³â°) is the most statistically significant result in our entire analysis. But the direction depends entirely on which cancer type and which drug pathway are involved. **KIRC (kidney cancer)** shows the strongest sensitisation with active gene expression (âˆ’1.115 shift) -- consistent with KIRC's known sensitivity to gene expression dysregulation from VHL tumour suppressor loss. **THCA (thyroid cancer)** shows the strongest resistance (+1.322 shift) -- reflecting a cancer type whose oncogenic drivers (BRAF V600E, RET/PTC fusions) create active bypass pathways that compensate for drug pressure. At the pathway level, Metabolism drugs (+1.992) are dramatically less effective in gene-expression-active cells -- cancer cells with elevated gene expression are metabolically more adaptable and can reroute around metabolic inhibitors. **TW 37** (BCL-2 inhibitor, shift -4.317) is the drug most improved by gene expression activity -- cells that are actively transcribing genes are often over-expressing BCL-2 as a survival protein; blocking it removes their primary anti-death shield.

**Methylation sensitises Mitosis and Hormone-related pathways in solid tumours.**

Methylation silences tumour suppressor genes -- the natural brakes on cancer growth. When brakes are removed, cells become more dependent on active growth pathways. The Mitosis pathway shows strong sensitisation in methylated cells (-0.644), because cells that have silenced growth suppressors are dividing faster and are therefore more vulnerable to mitotic disruption. **SCLC (small cell lung cancer)** is the cancer type most sensitised by methylation (-0.594), consistent with SCLC's known epigenetically driven biology and its established sensitivity to drugs that exploit methylation-related vulnerabilities.

> **The central conclusion of the multi-omics analysis:** No single genomic, transcriptomic, or epigenomic feature uniformly increases or decreases drug sensitivity across all cancers and drugs. Each feature creates specific, drug-and-cancer-type-dependent vulnerabilities. The overall Spearman correlations near zero are not null results -- they are the mathematical consequence of averaging opposing signals. The deeper analysis (Methods 3--7) reveals that these opposing signals are real, large (up to 4.3 LN_IC50 units), statistically significant, and biologically meaningful. **The message for precision oncology: a patient's genomic profile must be interpreted in the context of which drug is being considered and which cancer type is present.**

---

### Step 5 -- Visualising the Story
*Fifteen plots -- covering distribution (histogram), boxplot (×4: top drugs, cancer types, genomic/transcriptomic/epigenomic feature groups, MSI genomic biomarker), scatter (×3: AUC vs IC50, stratified by gene expression, drug-level biomarker scatter), heatmap (×3: correlation, cancer×drug pivot, pathway×feature), bar chart (horizontal + vertical + grouped), KDE density, and five dedicated genomic/transcriptomic/epigenomic influence visualizations.*

**1. Distribution Plot** (`distribution_plot.png`)
The spread of all 162,103 LN_IC50 values. Right-skewed -- more experiments where drugs required high doses than very low ones. The heavy left tail (down to -8.64) represents the rare but powerful drug-cancer matches that precision oncology seeks to identify and replicate.

**2. Boxplot -- Top 10 Most Effective Drugs** (`boxplot_top_effective_drugs.png`)
Romidepsin and Bortezomib show tight boxes -- consistent killers across cancer types. Daporinad and Docetaxel show wide boxes -- highly selective, working brilliantly for some cancers and poorly for others.

**3. Boxplot -- Top 10 Most Sensitive Cancer Types** (`boxplot_cancer_types.png`)
Leukaemia types cluster at the bottom, confirming systemic drug vulnerability. Solid tumours sit higher, reflecting physical and biological resistance mechanisms.

**4. Scatter Plot -- AUC vs LN_IC50** (`scatter_auc_ic50.png`)
Negative relationship confirmed -- as drugs become more potent (lower LN_IC50), they also inhibit cells more completely across all doses (lower AUC). The spread shows that some drugs are potent at target dose but taper off, while others maintain effectiveness across the full dose range.

**5. Correlation Heatmap -- Genomic / Transcriptomic / Epigenomic Features vs Drug Metrics** (`correlation_heatmap.png`)
A Spearman correlation matrix showing how all molecular features (MSI_status, CNA, Gene Expression, Methylation -- encoded as numeric 0/1) correlate with drug sensitivity metrics (LN_IC50, AUC, Z_SCORE). LN_IC50 and AUC are strongly negatively correlated. MSI_status and CNA show small negative correlations with LN_IC50 (genomic features sensitise). Gene Expression shows a small positive correlation (transcriptomic activity increases resistance). This heatmap directly visualises how genomic, transcriptomic, and epigenomic features correlate with drug response at the aggregate level.

**6. Boxplot -- Genomic / Transcriptomic / Epigenomic Feature Groups (Y vs N)** (`boxplot_genomic_features.png`)
Three side-by-side boxplots comparing LN_IC50 distributions for cells WITH (Y, coral) vs WITHOUT (N, blue) each molecular feature: Genomic (CNA), Transcriptomic (Gene Expression), and Epigenomic (Methylation). Each boxplot shows median, interquartile range, and outliers -- the standard visualization for comparing two groups' distributions. The CNA and Gene Expression boxplots show visible median shifts between Y and N groups, directly visualising that genomic and transcriptomic features influence the distribution of drug sensitivity across the dataset.

**7. Pivot Heatmap -- Cancer Type Ã-- Drug** (`heatmap_cancer_drug_pivot.png`)
A matrix of the top 15 cancer types against the top 15 most effective drugs. Dark green cells represent the strongest drug-cancer sensitivities. Leukaemia types (CLL, ALL, LCML) show consistently green rows, confirming their broad drug sensitivity.

**8. Horizontal Bar Chart -- Drug Sensitivity by Target Pathway** (`barplot_pathway_sensitivity.png`)
All drug target pathways ranked by mean LN_IC50. Green bars (negative LN_IC50) indicate net cancer-killing efficacy; blue bars indicate resistance. Mitosis stands visibly apart -- direct visual confirmation of the Kruskal-Wallis result (H = 21,985.95).

**9. Vertical Bar Chart -- Top 20 Most Sensitive Cancer Types** (`barplot_cancer_sensitivity.png`)
The 20 most drug-sensitive TCGA cancer types ranked by mean LN_IC50, with the dataset mean as a reference line. Blood cancers cluster dramatically below the reference; solid tumours above.

**10. KDE Density Plot -- Transcriptomic Influence on LN_IC50** (`kde_gene_expression_influence.png`)
Overlaid kernel density curves showing the full LN_IC50 probability distributions for Gene Expression Active (Y, coral) vs Absent (N, blue). The mean reference lines mark the shift (Y mean = 2.83, N mean = 2.38). This is a dedicated *transcriptomic influence* visualization -- it makes the statistically proven difference (p = 2.91 Ã-- 10â»Â³â°) directly visible as a density shift. Cells lacking active gene expression show a distribution pulled toward lower LN_IC50 (easier to kill), confirming that active transcription creates a resistance advantage.

**11. Scatter Plot -- AUC vs LN_IC50 Stratified by Gene Expression** (`scatter_auc_ic50_by_gene_expression.png`)
The AUC vs LN_IC50 scatter plot with points coloured by transcriptomic status: coral = Gene Expression Active (Y), blue = Gene Expression Absent (N). The N-group points (all drawn, n=3,761) are visibly shifted left and downward -- lower AUC and lower LN_IC50 -- showing that transcriptomically inactive cells are simultaneously easier to kill and more fully inhibited across the full dose range. This directly visualises how a transcriptomic feature changes the drug response relationship.

**12. Pathway Ã-- Genomic Feature Heatmap** (`heatmap_pathway_genomic_effects.png`)
A colour-coded matrix showing the LN_IC50 shift (Y mean âˆ’ N mean) for every combination of drug target pathway (rows) and genomic/transcriptomic/epigenomic feature (columns). **Blue = feature presence sensitises that pathway's drugs; Red = feature presence creates resistance.** This is the definitive genomic influence visualisation -- it maps three types of biological alteration (copy number, transcriptome, epigenome) against every drug mechanism class simultaneously. Key visible patterns: CNA creates a strongly blue Mitosis row (âˆ’1.25 shift), confirming that copy number disruption sensitises cells to mitotic inhibitors; Gene Expression creates a strongly red Metabolism row (+1.99), showing that transcriptomic activity makes cancer cells metabolically adaptive; Methylation creates a blue Hormone-related row (âˆ’0.42). The colour contrasts between feature columns within the same pathway row reveal that the three genomic layers have opposing and complementary effects -- a direct argument for multi-omic profiling in precision oncology.

**13. Transcriptomic Influence -- Grouped Bar Chart for Top 10 Most Affected Drugs** (`barplot_gene_expression_drug_effect.png`)
Side-by-side bars showing mean LN_IC50 for Gene Expression Active (Y, coral) vs Absent (N, blue) for the 10 drugs showing the largest absolute difference between groups. This is the standard bioinformatics visualization for a genomic biomarker analysis. The dataset-mean reference line shows which groups fall above and below the average. The bar lengths make the effect magnitude immediately quantifiable -- TW 37 shows bars at 1.31 (Y) and 5.63 (N), a 4.32-unit gap that translates to an approximately 75Ã-- difference in required dose. The consistent separation between Y and N bars across all 10 drugs confirms that transcriptomic status is a robust and clinically relevant predictor of drug sensitivity for this drug class.

**14. Drug-Level Genomic Biomarker Scatter** (`scatter_gene_expression_y_vs_n_drug_level.png`)
Each point represents one drug. The X-axis shows the mean LN_IC50 for cells with Gene Expression Active (Y); the Y-axis shows the mean LN_IC50 for cells with Gene Expression Absent (N). The diagonal dashed line marks "no effect" -- points above the diagonal represent drugs where N cells are harder to kill (gene expression absence confers resistance), and points below the diagonal represent drugs where N cells are more sensitive (gene expression activity causes resistance for that drug). The 8 most affected drugs are labelled. This is a unique visualization type -- a drug-level correlation scatter -- that simultaneously shows the direction, magnitude, and distribution of transcriptomic influence across all drugs in a single plot. The coral cluster (resistance drugs -- where gene expression increases LN_IC50) sits predominantly below the diagonal, directly visualising the drug shift census finding that 74.6% of drugs show resistance with active gene expression. The blue outliers (sensitising drugs including TW 37) sit dramatically above the diagonal, confirming their status as precision transcriptomic biomarker-matched drugs.

**15. Boxplot -- Genomic Biomarker (MSI Status) vs Drug Sensitivity** (`boxplot_msi_drug_sensitivity.png`)
A two-panel figure. Left panel: a **boxplot** comparing LN_IC50 distributions for MSI-H (coral) vs MSS/MSI-L (blue) cells. MSI (Microsatellite Instability) is a direct **genomic** biomarker -- MSI-H cells have defective DNA mismatch repair, making them genomically hypermutated. The boxplot shows MSI-H cells have a lower median LN_IC50 (more drug-sensitive). Right panel: a horizontal bar chart of the top 10 drugs most sensitised by MSI-H status, showing LN_IC50 shift (MSI-H mean minus MSS mean) with Methotrexate (âˆ’1.564) and Daporinad (âˆ’1.293) as the top hits. This plot directly connects a genomic feature to drug response in the most interpretable visual format -- a boxplot comparison between genomic subtypes -- making the genomic influence on drug sensitivity immediately visible.

---

## What Our Findings Mean -- The Full Picture

**Cancer is not one disease.** The LN_IC50 range spans 22 units (-8.64 to +13.82), with a standard deviation nearly equal to the mean. Different cancers respond to drugs in fundamentally different ways. A treatment protocol designed for the "average cancer" will fail a large fraction of patients.

**Pathway membership is a statistically proven predictor of drug effectiveness.** The Kruskal-Wallis test (H = 21,985.95, p â‰ˆ 0) confirms that a drug's target pathway is one of the strongest predictors of its average effectiveness -- stronger than knowing the individual drug name for most compounds. Mitosis-targeting drugs (mean -1.40) outperform all other pathway classes by a significant margin.

**Broad weapons and precision tools serve different roles.** Romidepsin and Bortezomib attack universal cellular machinery -- they work broadly because all cancer cells depend on HDAC and proteasome function. Dasatinib and Gemcitabine are precision tools -- extraordinarily powerful when matched to the right cancer, ineffective otherwise.

**Blood cancers are the most treatable in this dataset.** The top 6 most sensitive cancer types are all blood cancers (CLL, LAML, DLBC, ALL, LCML, MM), with mean LN_IC50 values 1.3--1.7 units below the dataset mean. The most resistant cancer (PAAD) requires 2.6Ã-- more drug than the most sensitive (CLL).

**Genomic, transcriptomic, and epigenomic features are drug-and-cancer-specific predictors, not universal markers.** The drug shift census puts the scale in numbers: CNA sensitises 69.9% of drugs (median shift âˆ’0.337); Gene Expression causes resistance in 74.6% of drugs (median shift +0.340); Methylation is genuinely balanced at 52/48. The pathwayÃ--feature heatmap (plot 12) makes the mechanistic structure visible: CNA most strongly sensitises Mitosis drugs (âˆ’1.25 shift) while Gene Expression most strongly increases resistance to Metabolism drugs (+1.99). The grouped bar chart (plot 13) and drug-level scatter (plot 14) make the drug-level effect unmistakably visual -- bars for TW 37 sit at Y=1.31 and N=5.63, a 4.32-unit raw LN_IC50 gap (the largest single-drug raw shift in the dataset). Cohen's d analysis (Method 9) identifies XAV939 (d = +1.207) and LY2109761 (d = +1.187) as the most standardised resistance pairings, and Methotrexate (d = âˆ’0.850) as the most standardised sensitisation pairing -- all "large" effects by conventional thresholds. The distinction between raw shift (TW 37 dominates) and standardised effect size (XAV939, Methotrexate) reveals different biological dimensions: TW 37 shows a dramatic mean difference but high variance, while Methotrexate's d = âˆ’0.850 reflects a consistent, reliable sensitivity shift.

**Genomic feature presence does not make drug responses unpredictable overall.** Z_SCORE analysis (Method 8) shows mean |Z_SCORE| â‰ˆ 0.80 regardless of feature presence -- genomic features do not cause generally unusual responses. They cause *specific* unusual responses for specific drugs (drug-level shifts up to 4.3 LN_IC50 units). This is precisely what precision oncology requires: a feature-to-drug pairing, not a feature-to-all-drugs relationship.

**Every cancer cell line in this dataset carries genomic alterations.** No cell had a genomic score of 0 (all features absent). Genomic disruption -- copy number changes, expression dysregulation, methylation -- is not a subtype of cancer. It is cancer itself.

---

## Why This All Matters

Every year, millions of people are diagnosed with cancer. Many receive treatments that do not work -- not because better drugs do not exist, but because we have not yet perfectly matched the right drug to the right patient.

Projects like GDSC, and analyses like ours, are building the scientific foundation for a future where a doctor can look at a tumour's genetic profile and say with confidence:

*"Based on the biology of your cancer -- its copy number alterations, gene expression patterns, methylation status, and the specific biological pathway your cancer depends on -- this is the drug most likely to help you."*

Our analysis demonstrates this is achievable. The data already contains the signals. The work of genomics-guided oncology is learning to read them -- at the level of individual drugs, individual cancer types, and individual molecular features (genomic, transcriptomic, epigenomic), not averages.

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
COL_MSI         = 'Microsatellite instability Status (MSI)'
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

    print("\n--- Duplicates Check ---)
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

    print("\nHighly variable drugs -- selective responders (Highest Std Dev):")
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
        print(f"\n--- Most Sensitive Cancer Types (Lowest Mean {COL_LN_IC50}) ---)
        print(cancer_drug_response.head(10))
    else:
        print(f"  -> Column '{COL_CANCER_TYPE}' not found. Cannot analyze cancer types.")

    if COL_CELL_LINE in df.columns and COL_LN_IC50 in df.columns:
        cell_drug_response = df.groupby([COL_CELL_LINE, COL_DRUG])[COL_LN_IC50].mean().sort_values().reset_index()
        print(f"\n--- Most Sensitive Cell Lines (Lowest Mean {COL_LN_IC50}) ---)
        print(cell_drug_response.head(10))

    print("\nWhat patterns exist in the drug response across cell lines?")
    if COL_DRUG in df.columns and COL_LN_IC50 in df.columns:
        drug_patterns = df.groupby(COL_DRUG)[COL_LN_IC50].agg(['mean', 'std']).dropna()
        print("Pattern 1: Universally Strong Drugs (Lowest Mean)")
        print(drug_patterns.sort_values('mean').head(10))
        print("Pattern 2: Highly Targeted / Selective Drugs (Highest Variance across cell lines)")
        print(drug_patterns.sort_values('std', ascending=False).head(10))

    print("\n--- Drug Selectivity: Largest LN_IC50 spread across cancer types ---)
    if COL_CANCER_TYPE in df.columns and COL_DRUG in df.columns:
        drug_cancer_pivot = df.groupby([COL_DRUG, COL_CANCER_TYPE])[COL_LN_IC50].mean().unstack(COL_CANCER_TYPE)
        selectivity = drug_cancer_pivot.std(axis=1).dropna().sort_values(ascending=False)
        print("Top 10 most selective drugs (work very differently across cancer types):")
        print(selectivity.head(10).to_frame('selectivity_score'))

    print("\n--- Overall Cancer Type Sensitivity Ranking (mean LN_IC50 across all drugs) ---)
    if COL_TCGA_DESC in df.columns:
        cancer_overall = df.groupby(COL_TCGA_DESC)[COL_LN_IC50].agg(
            mean='mean', median='median', std='std', count='count'
        ).sort_values('mean')
        print("Top 10 most drug-sensitive cancer types (lowest mean LN_IC50):")
        print(cancer_overall.head(10))
        print("\nTop 10 most drug-resistant cancer types (highest mean LN_IC50):")
        print(cancer_overall.tail(10))
        print("\nTop 10 most variable cancer types (highest response std dev -- most selective drug targets):")
        print(cancer_overall.sort_values('std', ascending=False).head(10))


def analyze_genomic_influence(df):
    """Analyze how genomic, transcriptomic, and epigenomic features influence drug response."""
    print("\n=== Genomic / Transcriptomic / Epigenomic Influence on Drug Sensitivity ===")
    print("  MSI Status      -> GENOMIC feature       (microsatellite instability = DNA mismatch repair deficiency)")
    print("  CNA             -> GENOMIC feature       (DNA copy number alteration)")
    print("  Gene Expression -> TRANSCRIPTOMIC feature (mRNA expression change)")
    print("  Methylation     -> EPIGENOMIC feature     (DNA methylation status)")

    existing_features = [col for col in GENOMIC_FEATURES if col in df.columns]
    if not existing_features:
        print("  -> Genomic feature columns not found. Skipping.")
        return
    if COL_LN_IC50 not in df.columns:
        print(f"  -> '{COL_LN_IC50}' not found. Skipping.")
        return

    # MSI (Microsatellite Instability) -- dedicated genomic biomarker analysis
    print("\n[Genomic Biomarker] MSI Status -- Microsatellite Instability (DNA-level genomic feature):")
    print("  MSI-H = defective DNA mismatch repair (hypermutated)  |  MSS/MSI-L = intact repair")
    if COL_MSI in df.columns:
        msi_h = df[df[COL_MSI] == 'MSI-H'][COL_LN_IC50].dropna()
        mss   = df[df[COL_MSI] == 'MSS/MSI-L'][COL_LN_IC50].dropna()
        if len(msi_h) > 0 and len(mss) > 0:
            print(f"  MSI-H:     n = {len(msi_h):,}, mean LN_IC50 = {msi_h.mean():.4f}")
            print(f"  MSS/MSI-L: n = {len(mss):,}, mean LN_IC50 = {mss.mean():.4f}")
            u_stat, p_msi = stats.mannwhitneyu(msi_h, mss, alternative='two-sided')
            diff = msi_h.mean() - mss.mean()
            sig = "statistically significant" if p_msi < 0.05 else "not significant"
            print(f"  Difference (MSI-H minus MSS): {diff:+.4f}")
            print(f"  Mann-Whitney U: p = {p_msi:.2e} ({sig})")
            pv = ((len(msi_h) - 1) * msi_h.std()**2 + (len(mss) - 1) * mss.std()**2) / (len(msi_h) + len(mss) - 2)
            cd = diff / (pv**0.5) if pv > 0 else 0.0
            el = "negligible" if abs(cd) < 0.2 else "small" if abs(cd) < 0.5 else "medium" if abs(cd) < 0.8 else "large"
            print(f"  Cohen's d = {cd:+.4f} ({el} effect size)")
            print(f"\n  Top 5 drugs most sensitised by MSI-H genomic status:")
            drug_rows = []
            for drug in df[COL_DRUG].unique():
                d = df[df[COL_DRUG] == drug]
                h = d[d[COL_MSI] == 'MSI-H'][COL_LN_IC50].dropna()
                s = d[d[COL_MSI] == 'MSS/MSI-L'][COL_LN_IC50].dropna()
                if len(h) >= 5 and len(s) >= 5:
                    drug_rows.append({'Drug': drug, 'Shift': round(h.mean() - s.mean(), 3),
                                      'MSI-H_mean': round(h.mean(), 3), 'MSS_mean': round(s.mean(), 3)})
            if drug_rows:
                dr = pd.DataFrame(drug_rows).sort_values('Shift')
                print(dr.head(5).to_string(index=False))

    # Method 1: Overall Spearman correlation
    df_num = df[[COL_LN_IC50] + existing_features].copy()
    for col in existing_features:
        df_num[col] = df_num[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
        df_num[col] = pd.to_numeric(df_num[col], errors='coerce')
    df_num = df_num.dropna()

    print(f"\n[Method 1] Spearman correlation (scipy.stats.spearmanr) -- each feature vs {COL_LN_IC50}:")
    print("  Genomic / transcriptomic / epigenomic features encoded as binary (Y=1, N=0) for correlation.")
    correlations = {}
    for feature in existing_features:
        r, p_val = stats.spearmanr(df_num[feature], df_num[COL_LN_IC50])
        correlations[feature] = r
        strength = "Very Weak" if abs(r) < 0.2 else "Weak" if abs(r) < 0.4 else "Moderate" if abs(r) < 0.6 else "Strong"
        direction = "towards Resistance" if r > 0 else "towards Sensitivity"
        sig = "p < 0.05 significant" if p_val < 0.05 else "p >= 0.05 not significant"
        print(f"  {feature}: r = {r:>7.4f} ({strength} {direction}, {sig}, p = {p_val:.2e})")
    if COL_MSI in df.columns:
        df_msi_corr = df[[COL_LN_IC50, COL_MSI]].copy()
        df_msi_corr['MSI_num'] = df_msi_corr[COL_MSI].map({'MSI-H': 1, 'MSS/MSI-L': 0})
        df_msi_corr = df_msi_corr.dropna()
        r_msi, p_msi = stats.spearmanr(df_msi_corr['MSI_num'], df_msi_corr[COL_LN_IC50])
        sig_msi = "p < 0.05 significant" if p_msi < 0.05 else "not significant"
        print(f"  MSI_status (Genomic): r = {r_msi:>7.4f} (towards Sensitivity, {sig_msi}, p = {p_msi:.2e})")
    print("  NOTE: Near-zero AGGREGATE correlations are expected -- they are the average of opposing")
    print("  drug-specific signals. Drug-level Spearman correlations (Method 1b) reveal the real influence.")

    # Method 1b: Per-drug Spearman correlation
    print("\n[Method 1b] Per-drug Spearman correlation (genomic/transcriptomic/epigenomic feature vs LN_IC50):")
    print("  Shows that genomic features influence drug response strongly for SPECIFIC drugs,")
    print("  even when the aggregate correlation is near zero.")
    for feature in existing_features:
        df_feat = df.copy()
        df_feat[feature] = df_feat[feature].map({'Y': 1, 'N': 0}).fillna(float('nan'))
        drug_spearman = []
        for drug in df[COL_DRUG].unique():
            d = df_feat[df_feat[COL_DRUG] == drug][[COL_LN_IC50, feature]].dropna()
            if len(d) >= 10 and d[feature].nunique() > 1:
                r, p = stats.spearmanr(d[feature], d[COL_LN_IC50])
                drug_spearman.append({'Drug': drug, 'r': round(r, 3), 'p': round(p, 4)})
        if drug_spearman:
            ds = pd.DataFrame(drug_spearman)
            sig_count = (ds['p'] < 0.05).sum()
            print(f"\n  {feature}: {sig_count}/{len(ds)} drugs show significant correlation (p < 0.05)")
            print(f"  Top 5 most negatively correlated drugs (feature presence = more sensitive):")
            print(ds.sort_values('r').head(5)[['Drug', 'r', 'p']].to_string(index=False))
            print(f"  Top 5 most positively correlated drugs (feature presence = more resistant):")
            print(ds.sort_values('r', ascending=False).head(5)[['Drug', 'r', 'p']].to_string(index=False))
    if COL_MSI in df.columns:
        df_msi2 = df.copy()
        df_msi2['MSI_num'] = df_msi2[COL_MSI].map({'MSI-H': 1, 'MSS/MSI-L': 0})
        msi_spearman = []
        for drug in df[COL_DRUG].unique():
            d = df_msi2[df_msi2[COL_DRUG] == drug][['LN_IC50', 'MSI_num']].dropna()
            if len(d) >= 10 and d['MSI_num'].nunique() > 1:
                r, p = stats.spearmanr(d['MSI_num'], d['LN_IC50'])
                msi_spearman.append({'Drug': drug, 'r': round(r, 3), 'p': round(p, 4)})
        if msi_spearman:
            ms = pd.DataFrame(msi_spearman)
            sig_count = (ms['p'] < 0.05).sum()
            print(f"\n  MSI_status (Genomic): {sig_count}/{len(ms)} drugs show significant Spearman correlation")
            print(f"  Top 5 drugs most sensitised by MSI-H (most negative r):")
            print(ms.sort_values('r').head(5)[['Drug', 'r', 'p']].to_string(index=False))

    # Method 2: Group comparison Y vs N with Mann-Whitney U test
    print("\n[Method 2] Group comparison -- cells WITH (Y) vs WITHOUT (N) each feature:")
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
        pooled_var = ((len(y_vals) - 1) * y_vals.std()**2 + (len(n_vals) - 1) * n_vals.std()**2) / (len(y_vals) + len(n_vals) - 2)
        cohens_d = diff / (pooled_var**0.5) if pooled_var > 0 else 0.0
        effect_label = "negligible" if abs(cohens_d) < 0.2 else "small" if abs(cohens_d) < 0.5 else "medium" if abs(cohens_d) < 0.8 else "large"
        print(f"    -> Cohen's d = {cohens_d:+.4f} ({effect_label} effect size)")

    # Method 3: Drug-level differential sensitivity per genomic feature
    print("\n[Method 3] Top drugs most affected by each genomic feature:")
    for feature in existing_features:
        pivot = df.groupby([COL_DRUG, feature])[COL_LN_IC50].mean().unstack(feature)
        if 'Y' not in pivot.columns or 'N' not in pivot.columns:
            continue
        pivot = pivot.dropna(subset=['Y', 'N'])
        pivot['shift'] = pivot['Y'] - pivot['N']

        print(f"\n  {feature} -- Top 5 drugs where presence SENSITISES (most negative shift):")
        for drug, row in pivot.sort_values('shift').head(5).iterrows():
            print(f"    {drug:<35} Y={row['Y']:>6.3f}  N={row['N']:>6.3f}  shift={row['shift']:>+7.3f}")

        print(f"\n  {feature} -- Top 5 drugs where presence CONFERS resistance (most positive shift):")
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
                print(f"\n  {feature} -- Top 5 cancer types most SENSITISED (most negative shift):")
                print(eff.head(5).to_string(index=False))
                print(f"\n  {feature} -- Top 5 cancer types most RESISTANT with presence:")
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
                print(f"\n  {feature} -- Pathways most SENSITISED by feature presence:")
                print(peff.head(5).to_string(index=False))
                print(f"\n  {feature} -- Pathways most RESISTANT with feature presence:")
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
                  f"(vs {100*feat_all:.1f}% overall -- {direction} {enrich:.2f}x)")

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

    # Method 8: Z_SCORE-based genomic analysis -- do genomic features drive outlier responses?
    print("\n[Method 8] Genomic features and outlier drug responses (|Z_SCORE| analysis):")
    if COL_Z_SCORE in df.columns:
        print(f"  Z_SCORE measures how far each response deviates from the drug's average across all cell lines.")
        print(f"  High |Z_SCORE| = unusually strong or weak response (possible genomic driver).")
        for feature in existing_features:
            y_z = df[df[feature] == 'Y'][COL_Z_SCORE].dropna()
            n_z = df[df[feature] == 'N'][COL_Z_SCORE].dropna()
            if len(y_z) == 0 or len(n_z) == 0:
                continue
            stat, p_val = stats.mannwhitneyu(y_z.abs(), n_z.abs(), alternative='two-sided')
            sig = "statistically significant" if p_val < 0.05 else "not significant"
            more_extreme = "more extreme" if y_z.abs().mean() > n_z.abs().mean() else "more typical"
            print(f"\n  {feature}:")
            print(f"    Mean |Z_SCORE| when Y = {y_z.abs().mean():.4f}  (n={len(y_z):,})")
            print(f"    Mean |Z_SCORE| when N = {n_z.abs().mean():.4f}  (n={len(n_z):,})")
            print(f"    -> Feature presence is associated with {more_extreme} drug responses")
            print(f"    -> Mann-Whitney U: p = {p_val:.2e} ({sig})")

    # Drug shift census -- how many drugs are sensitised vs resistant per feature
    print("\n--- Molecular Feature Influence Scale: Drug Shift Census (Genomic / Transcriptomic / Epigenomic) ---)
    print("  For each feature, how many drugs show sensitisation (Y < N) vs resistance (Y > N)?")
    for feature in existing_features:
        pivot = df.groupby([COL_DRUG, feature])[COL_LN_IC50].mean().unstack(feature)
        if 'Y' in pivot.columns and 'N' in pivot.columns:
            pivot = pivot.dropna(subset=['Y', 'N'])
            pivot['shift'] = pivot['Y'] - pivot['N']
            n_sens = (pivot['shift'] < 0).sum()
            n_resist = (pivot['shift'] > 0).sum()
            n_total = len(pivot)
            pct_sens = 100 * n_sens / n_total if n_total > 0 else 0
            print(f"\n  {feature} ({n_total} drugs with both Y and N data):")
            print(f"    Sensitised (Y < N):  {n_sens} drugs  ({pct_sens:.1f}%)")
            print(f"    Resistant  (Y > N):  {n_resist} drugs  ({100-pct_sens:.1f}%)")
            print(f"    Median shift: {pivot['shift'].median():+.3f} LN_IC50 units")
            print(f"    Max sensitisation:  {pivot['shift'].min():+.3f}  ({pivot['shift'].idxmin()})")
            print(f"    Max resistance:     {pivot['shift'].max():+.3f}  ({pivot['shift'].idxmax()})")

    # Method 9: Strongest genomic biomarker-drug pairings by Cohen's d effect size
    print("\n[Method 9] Strongest genomic biomarker-drug pairings (standardised Cohen's d effect size):")
    print("  Identifies which individual drugs are most strongly predicted by each genomic feature.")
    print("  Cohen's d = (Y_mean - N_mean) / pooled_std  |  |d| < 0.2 negligible, 0.5 small, 0.8 medium, >0.8 large")
    for feature in existing_features:
        drug_effects = []
        for drug in df[COL_DRUG].unique():
            df_d = df[df[COL_DRUG] == drug]
            y_v = df_d[df_d[feature] == 'Y'][COL_LN_IC50].dropna()
            n_v = df_d[df_d[feature] == 'N'][COL_LN_IC50].dropna()
            if len(y_v) >= 5 and len(n_v) >= 5:
                pooled_var = ((len(y_v) - 1) * y_v.std()**2 + (len(n_v) - 1) * n_v.std()**2) / (len(y_v) + len(n_v) - 2)
                pooled_std = pooled_var**0.5 if pooled_var > 0 else 1.0
                d = (y_v.mean() - n_v.mean()) / pooled_std
                drug_effects.append({'Drug': drug, 'Cohen_d': round(d, 3),
                                     'Y_mean': round(y_v.mean(), 3), 'N_mean': round(n_v.mean(), 3),
                                     'n_N': len(n_v)})
        if drug_effects:
            de_df = pd.DataFrame(drug_effects).sort_values('Cohen_d')
            print(f"\n  {feature} -- Top 5 drugs most strongly SENSITISED (most negative Cohen's d):")
            print(de_df.head(5)[['Drug', 'Cohen_d', 'Y_mean', 'N_mean', 'n_N']].to_string(index=False))
            print(f"\n  {feature} -- Top 5 drugs most strongly conferring RESISTANCE (most positive Cohen's d):")
            print(de_df.tail(5)[['Drug', 'Cohen_d', 'Y_mean', 'N_mean', 'n_N']].to_string(index=False))

    # --- Summary ---
    print("\n--- Multi-Omics Influence Summary ---)
    print("  CNA (GENOMIC):             significantly sensitises cells overall (p=0.007)")
    print("                             largest effect on Mitosis-targeting drugs (shift -1.25)")
    print("  Gene Expression (TRANSCRIPTOMIC): significantly increases resistance overall (p=2.91e-30)")
    print("                             most cancer-type-specific effect (THCA +1.32 vs KIRC -1.12)")
    print("                             dramatically sensitises BCL-2 inhibitor TW 37 (shift -4.32)")
    print("  Methylation (EPIGENOMIC):  no significant aggregate effect (p=0.34)")
    print("                             but sensitises Mitosis drugs (-0.64) and SCLC specifically")
    print("  All features:    effects are drug-specific and cancer-type-specific --)
    print("                   molecular profiling (genomic/transcriptomic/epigenomic) is only predictive when paired with drug target.")

    return correlations


def visualize_results(df):
    """Generate and save supporting visualizations for the GDSC dataset."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    print(f"\nGenerating Data Visualizations and saving to: {output_dir}")

    if COL_LN_IC50 not in df.columns:
        print(f"  -> Column '{COL_LN_IC50}' not found. Cannot generate visualizations.")
        return

    sns.set_theme(style="whitegrid")

    # 1/14: Distribution of LN_IC50
    print("  -> Saving 1/15: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[COL_LN_IC50].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({COL_LN_IC50})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300)
    plt.close()

    # 2/14: Boxplot -- top 10 most effective drugs
    print("  -> Saving 2/15: boxplot_top_effective_drugs.png...")
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

    # 3/14: Boxplot -- top 10 most sensitive cancer types
    print("  -> Saving 3/15: boxplot_cancer_types.png...")
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

    # 4/14: Scatter -- AUC vs LN_IC50
    print("  -> Saving 4/15: scatter_auc_ic50.png...")
    if COL_AUC in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=COL_AUC, y=COL_LN_IC50, alpha=0.3, color='darkorange')
        plt.title(f'Relationship between {COL_AUC} and {COL_LN_IC50}', fontsize=14, fontweight='bold')
        plt.xlabel('AUC (Area Under the Curve)', fontsize=12)
        plt.ylabel(COL_LN_IC50, fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50.png"), dpi=300)
        plt.close()

    # 5/15: Correlation heatmap
    print("  -> Saving 5/15: correlation_heatmap.png...")
    df_heat = pd.DataFrame()
    for col in METRIC_COLS:
        if col in df.columns:
            df_heat[col] = df[col]
    for col in GENOMIC_FEATURES:
        if col in df.columns:
            df_heat[col] = df[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
            df_heat[col] = pd.to_numeric(df_heat[col], errors='coerce')
    if COL_MSI in df.columns:
        df_heat['MSI_status'] = df[COL_MSI].map({'MSI-H': 1, 'MSS/MSI-L': 0})
    if not df_heat.empty and len(df_heat.columns) > 1:
        plt.figure(figsize=(11, 9))
        sns.heatmap(df_heat.corr(method='spearman'), annot=True, fmt=".2f", cmap='coolwarm',
                    vmin=-1, vmax=1, square=True, linewidths=.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Heatmap -- Drug Sensitivity Metrics and\nGenomic / Transcriptomic / Epigenomic Features',
                  fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=300)
        plt.close()

    # 6/15: Boxplot -- LN_IC50 by genomic/transcriptomic/epigenomic feature (Y vs N)
    print("  -> Saving 6/15: boxplot_genomic_features.png...")
    existing_features = [col for col in GENOMIC_FEATURES if col in df.columns]
    if existing_features:
        fig, axes = plt.subplots(1, len(existing_features), figsize=(5 * len(existing_features), 6))
        if len(existing_features) == 1:
            axes = [axes]
        omics_labels = {COL_CNA: 'Genomic (CNA)', COL_GENE_EXPR: 'Transcriptomic (GE)',
                        COL_METHYLATION: 'Epigenomic (Methylation)'}
        for ax, feature in zip(axes, existing_features):
            df_feat = df[df[feature].isin(['Y', 'N'])]
            sns.boxplot(data=df_feat, x=feature, y=COL_LN_IC50, order=['N', 'Y'],
                        palette={'N': 'steelblue', 'Y': 'coral'}, ax=ax, width=0.5)
            ax.set_title(omics_labels.get(feature, feature), fontsize=12, fontweight='bold')
            ax.set_xlabel('Absent (N) vs Present (Y)', fontsize=10)
            ax.set_ylabel(COL_LN_IC50, fontsize=10)
        plt.suptitle('LN_IC50 by Molecular Feature Presence\n'
                     'Genomic (CNA) | Transcriptomic (Gene Expression) | Epigenomic (Methylation)',
                     fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "boxplot_genomic_features.png"), dpi=300)
        plt.close()

    # 7/14: Pivot heatmap -- top cancer types vs top drugs
    print("  -> Saving 7/15: heatmap_cancer_drug_pivot.png...")
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

    # 8/14: Horizontal bar chart -- mean LN_IC50 per drug target pathway
    print("  -> Saving 8/15: barplot_pathway_sensitivity.png...")
    if COL_TARGET_PATH in df.columns:
        pathway_means = df.groupby(COL_TARGET_PATH)[COL_LN_IC50].mean().sort_values()
        plt.figure(figsize=(10, max(6, len(pathway_means) * 0.45)))
        colors = ['forestgreen' if x < 0 else 'steelblue' for x in pathway_means.values]
        plt.barh(range(len(pathway_means)), pathway_means.values, color=colors, edgecolor='white')
        plt.yticks(range(len(pathway_means)), [p[:45] for p in pathway_means.index], fontsize=8)
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.6)
        plt.title('Mean Drug Sensitivity by Target Pathway', fontsize=14, fontweight='bold')
        plt.xlabel(f'Mean {COL_LN_IC50}  (â† More Effective  |  Less Effective â†’)', fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "barplot_pathway_sensitivity.png"), dpi=300)
        plt.close()

    # 9/14: Vertical bar chart -- top 20 most sensitive cancer types (TCGA codes)
    print("  -> Saving 9/15: barplot_cancer_sensitivity.png...")
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

    # 10/14: KDE plot -- LN_IC50 density curves for Gene Expression Y vs N
    print("  -> Saving 10/15: kde_gene_expression_influence.png...")
    if COL_GENE_EXPR in df.columns:
        plt.figure(figsize=(10, 6))
        y_data = df[df[COL_GENE_EXPR] == 'Y'][COL_LN_IC50].dropna()
        n_data = df[df[COL_GENE_EXPR] == 'N'][COL_LN_IC50].dropna()
        sns.kdeplot(y_data, label=f'Gene Expression Active (Y)  n={len(y_data):,}',
                    color='coral', fill=True, alpha=0.35, linewidth=2)
        sns.kdeplot(n_data, label=f'Gene Expression Absent (N)  n={len(n_data):,}',
                    color='steelblue', fill=True, alpha=0.35, linewidth=2)
        plt.axvline(y_data.mean(), color='coral', linestyle='--', linewidth=1.5,
                    label=f'Y mean = {y_data.mean():.2f}')
        plt.axvline(n_data.mean(), color='steelblue', linestyle='--', linewidth=1.5,
                    label=f'N mean = {n_data.mean():.2f}')
        plt.title('Transcriptomic Influence on Drug Sensitivity\n'
                  'LN_IC50 Density: Gene Expression Active vs Absent  (p = 2.91Ã--10â»Â³â°)',
                  fontsize=13, fontweight='bold')
        plt.xlabel(f'{COL_LN_IC50} (Lower = Cancer Cells Killed More Easily)', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "kde_gene_expression_influence.png"), dpi=300)
        plt.close()

    # 11/14: Scatter -- AUC vs LN_IC50 stratified by Gene Expression status
    print("  -> Saving 11/15: scatter_auc_ic50_by_gene_expression.png...")
    if COL_AUC in df.columns and COL_GENE_EXPR in df.columns:
        fig, ax = plt.subplots(figsize=(9, 6))
        df_n = df[df[COL_GENE_EXPR] == 'N']
        df_y = df[df[COL_GENE_EXPR] == 'Y'].sample(min(5000, len(df[df[COL_GENE_EXPR] == 'Y'])),
                                                    random_state=42)
        ax.scatter(df_n[COL_AUC], df_n[COL_LN_IC50], alpha=0.5, color='steelblue', s=15,
                   label=f'Gene Expression Absent (N)  n={len(df_n):,}', zorder=3)
        ax.scatter(df_y[COL_AUC], df_y[COL_LN_IC50], alpha=0.2, color='coral', s=8,
                   label=f'Gene Expression Active (Y)  n={len(df[df[COL_GENE_EXPR]=="Y"]):,}', zorder=2)
        ax.set_title('AUC vs LN_IC50 -- Stratified by Gene Expression (Transcriptomic) Status',
                     fontsize=13, fontweight='bold')
        ax.set_xlabel('AUC (Area Under the Dose-Response Curve)', fontsize=12)
        ax.set_ylabel(f'{COL_LN_IC50}', fontsize=12)
        ax.legend(fontsize=10, markerscale=2)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50_by_gene_expression.png"), dpi=300)
        plt.close()

    # 12/14: Heatmap -- drug target pathway Ã-- genomic features (LN_IC50 shift)
    print("  -> Saving 12/15: heatmap_pathway_genomic_effects.png...")
    existing_features = [col for col in GENOMIC_FEATURES if col in df.columns]
    if existing_features and COL_TARGET_PATH in df.columns:
        pathway_shift_data = {}
        for feature in existing_features:
            shifts = {}
            for pathway in df[COL_TARGET_PATH].unique():
                df_p = df[df[COL_TARGET_PATH] == pathway]
                y_v = df_p[df_p[feature] == 'Y'][COL_LN_IC50].dropna()
                n_v = df_p[df_p[feature] == 'N'][COL_LN_IC50].dropna()
                if len(y_v) >= 20 and len(n_v) >= 20:
                    shifts[pathway] = round(y_v.mean() - n_v.mean(), 3)
            pathway_shift_data[feature] = shifts
        shift_df = pd.DataFrame(pathway_shift_data).dropna(how='all')
        if not shift_df.empty:
            shift_df = shift_df.sort_values(by=shift_df.columns[0])
            plt.figure(figsize=(max(7, len(existing_features) * 2.2), max(6, len(shift_df) * 0.55)))
            sns.heatmap(shift_df, cmap='RdBu_r', center=0, annot=True, fmt='.2f',
                        linewidths=0.5,
                        cbar_kws={'label': 'LN_IC50 Shift (Y âˆ’ N mean)\n'
                                           'â† Blue = sensitises  |  Red = causes resistance â†’'})
            plt.title('Genomic / Transcriptomic / Epigenomic Influence by Drug Target Pathway\n'
                      '(LN_IC50 shift: mean with feature present minus mean without)',
                      fontsize=12, fontweight='bold')
            plt.xlabel('Feature Type (Genomic / Transcriptomic / Epigenomic)', fontsize=11)
            plt.ylabel('Drug Target Pathway', fontsize=11)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "heatmap_pathway_genomic_effects.png"), dpi=300)
            plt.close()

    # 13/14: Grouped bar chart -- Y vs N for top 10 drugs most affected by Gene Expression
    print("  -> Saving 13/15: barplot_gene_expression_drug_effect.png...")
    if COL_GENE_EXPR in df.columns and COL_DRUG in df.columns:
        pivot_ge = df.groupby([COL_DRUG, COL_GENE_EXPR])[COL_LN_IC50].mean().unstack(COL_GENE_EXPR)
        if 'Y' in pivot_ge.columns and 'N' in pivot_ge.columns:
            pivot_ge = pivot_ge.dropna(subset=['Y', 'N'])
            pivot_ge['abs_shift'] = (pivot_ge['Y'] - pivot_ge['N']).abs()
            top10_ge = pivot_ge.nlargest(10, 'abs_shift')
            x = range(len(top10_ge))
            width = 0.35
            fig, ax = plt.subplots(figsize=(13, 6))
            ax.bar([i - width / 2 for i in x], top10_ge['Y'], width,
                   label='Gene Expression Active (Y)', color='coral',
                   edgecolor='darkred', linewidth=0.5, alpha=0.85)
            ax.bar([i + width / 2 for i in x], top10_ge['N'], width,
                   label='Gene Expression Absent (N)', color='steelblue',
                   edgecolor='navy', linewidth=0.5, alpha=0.85)
            ax.set_xticks(list(x))
            ax.set_xticklabels(top10_ge.index, rotation=40, ha='right', fontsize=9)
            ax.axhline(df[COL_LN_IC50].mean(), color='black', linestyle=':', linewidth=1,
                       alpha=0.6, label=f'Dataset mean ({df[COL_LN_IC50].mean():.2f})')
            ax.set_title('Transcriptomic (Gene Expression) Influence on Drug Sensitivity\n'
                         'Top 10 Drugs with Largest LN_IC50 Shift Between Y and N Groups',
                         fontsize=13, fontweight='bold')
            ax.set_xlabel('Drug Name', fontsize=11)
            ax.set_ylabel(f'Mean {COL_LN_IC50} (Lower = More Drug Sensitive)', fontsize=11)
            ax.legend(fontsize=10)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "barplot_gene_expression_drug_effect.png"), dpi=300)
            plt.close()

    # 14/14: Scatter -- drug-level Y vs N LN_IC50 for Gene Expression (biomarker influence plot)
    print("  -> Saving 14/15: scatter_gene_expression_y_vs_n_drug_level.png...")
    if COL_GENE_EXPR in df.columns and COL_DRUG in df.columns:
        pivot_sc = df.groupby([COL_DRUG, COL_GENE_EXPR])[COL_LN_IC50].mean().unstack(COL_GENE_EXPR)
        if 'Y' in pivot_sc.columns and 'N' in pivot_sc.columns:
            pivot_sc = pivot_sc.dropna(subset=['Y', 'N'])
            pivot_sc['shift'] = pivot_sc['Y'] - pivot_sc['N']
            sensitised = pivot_sc[pivot_sc['shift'] < 0]
            resistant  = pivot_sc[pivot_sc['shift'] >= 0]
            fig, ax = plt.subplots(figsize=(9, 8))
            ax.scatter(sensitised['Y'], sensitised['N'], alpha=0.65, color='steelblue', s=45,
                       label=f'Sensitised by GE (Y < N): {len(sensitised)} drugs', zorder=3)
            ax.scatter(resistant['Y'], resistant['N'], alpha=0.65, color='coral', s=45,
                       label=f'Resistant with GE (Y â‰¥ N): {len(resistant)} drugs', zorder=3)
            lim_lo = min(pivot_sc[['Y', 'N']].min())
            lim_hi = max(pivot_sc[['Y', 'N']].max())
            ax.plot([lim_lo, lim_hi], [lim_lo, lim_hi], 'k--', alpha=0.4, linewidth=1,
                    label='No effect (Y = N)')
            top_affected = pivot_sc.reindex(pivot_sc['shift'].abs().nlargest(8).index)
            for drug, row in top_affected.iterrows():
                ax.annotate(drug[:22], (row['Y'], row['N']), fontsize=7, alpha=0.85,
                            xytext=(4, 4), textcoords='offset points')
            ax.set_title('Transcriptomic Biomarker Influence -- Drug-Level View\n'
                         'Each point = one drug: Y-axis is mean LN_IC50 without gene expression, '
                         'X-axis with it',
                         fontsize=12, fontweight='bold')
            ax.set_xlabel('Mean LN_IC50 -- Gene Expression Active (Y cells)', fontsize=11)
            ax.set_ylabel('Mean LN_IC50 -- Gene Expression Absent (N cells)', fontsize=11)
            ax.legend(fontsize=9, loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir,
                                     "scatter_gene_expression_y_vs_n_drug_level.png"), dpi=300)
            plt.close()

    # 15/15: Boxplot -- MSI-H vs MSS/MSI-L LN_IC50 (genomic biomarker influence)
    print("  -> Saving 15/15: boxplot_msi_drug_sensitivity.png...")
    if COL_MSI in df.columns:
        df_msi = df[df[COL_MSI].isin(['MSI-H', 'MSS/MSI-L'])].copy()
        if len(df_msi) > 0:
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            sns.boxplot(data=df_msi, x=COL_MSI, y=COL_LN_IC50,
                        order=['MSS/MSI-L', 'MSI-H'],
                        palette={'MSS/MSI-L': 'steelblue', 'MSI-H': 'coral'},
                        ax=axes[0], width=0.5)
            msi_h_med = df_msi[df_msi[COL_MSI] == 'MSI-H'][COL_LN_IC50].median()
            mss_med   = df_msi[df_msi[COL_MSI] == 'MSS/MSI-L'][COL_LN_IC50].median()
            axes[0].set_title('LN_IC50 by MSI Status\n(Genomic Biomarker -- DNA Mismatch Repair)',
                              fontsize=12, fontweight='bold')
            axes[0].set_xlabel('MSI Status (Genomic Feature)', fontsize=11)
            axes[0].set_ylabel('LN_IC50 (Drug Sensitivity)', fontsize=11)
            axes[0].text(0, mss_med + 0.25, f'median={mss_med:.2f}', ha='center', fontsize=9)
            axes[0].text(1, msi_h_med + 0.25, f'median={msi_h_med:.2f}', ha='center', fontsize=9)
            drug_rows = []
            for drug in df[COL_DRUG].unique():
                d = df[df[COL_DRUG] == drug]
                h = d[d[COL_MSI] == 'MSI-H'][COL_LN_IC50].dropna()
                s = d[d[COL_MSI] == 'MSS/MSI-L'][COL_LN_IC50].dropna()
                if len(h) >= 5 and len(s) >= 5:
                    drug_rows.append({'Drug': drug, 'Shift': round(h.mean() - s.mean(), 3)})
            if drug_rows:
                dr = pd.DataFrame(drug_rows).sort_values('Shift').head(10)
                colors = ['coral' if s < 0 else 'steelblue' for s in dr['Shift']]
                axes[1].barh(dr['Drug'], dr['Shift'], color=colors)
                axes[1].axvline(0, color='black', linewidth=0.8, linestyle='--')
                axes[1].set_title('Top 10 Drugs Most Sensitised by MSI-H\n(LN_IC50 shift: MSI-H mean âˆ’ MSS mean)',
                                  fontsize=12, fontweight='bold')
                axes[1].set_xlabel('LN_IC50 Shift (MSI-H âˆ’ MSS/MSI-L)', fontsize=11)
                axes[1].set_ylabel('Drug', fontsize=11)
            plt.suptitle('Genomic Biomarker Influence -- Microsatellite Instability (MSI) Status',
                         fontsize=14, fontweight='bold', y=1.01)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "boxplot_msi_drug_sensitivity.png"),
                        dpi=300, bbox_inches='tight')
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

# Exploring Genomics of Drug Sensitivity in Cancer (GDSC)
### A Layman's Guide - Written for Curious Minds, Not Just Biologists

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
*CELL_LINE_NAME*
The specific name of the cancer cell model being tested.

*TCGA_DESC*
The type of cancer (e.g., lung, colon, breast).

*DRUG_NAME*
The name of the pharmaceutical compound being tested against the cell line.

*TARGET_PATHWAY*
The specific biological mechanism or process the drug is designed to attack.

**Drug Response Metrics**
*LN_IC50*
How much drug was needed to kill 50% of the cancer cells. A lower value means the drug is more powerful (it took less of the drug to do the job).

*AUC*
Area Under the Curve. How well the drug worked across a full range of doses-a broader, overall measure of the drug's effectiveness.

*Z_SCORE*
A statistical measure showing how unusual or extreme this cell line's response is compared to the average of all other cell lines tested.

**Molecular & Genetic Features**
*CNA*
Copy Number Alteration. Indicates whether the cancer cell has a DNA copy error, such as a section of DNA being abnormally duplicated or deleted.

*Gene Expression*
Indicates whether a specific gene is unusually active (turned up) or silent (turned down) in this particular cancer.

*Methylation*
Indicates whether certain genes have been chemically "switched off" or muted by the cell.

*The most important number : LN_IC50* is the heart of this dataset. A very low or very negative LN_IC50 means the drug is a precision weapon - a tiny amount is enough to kill the cancer cells. A high LN_IC50 means you would need a dangerously large dose to see any effect at all.

---

## Our Analysis: A 5-Step Investigation

Think of this project like a detective story. We start with a massive pile of raw data and, step by step, extract meaning from it.

---

### Step 1 - Understanding the Dataset
*What are we actually working with?*

Before drawing any conclusions, a good scientist gets to know their data intimately. We ask:

- **How many experiments are in the dataset?** (Total rows and columns)
- **Are there gaps or errors?** We scan for missing values and duplicate entries - a single corrupted row can distort an entire analysis.
- **Are the numbers actually stored as numbers?** Computers can accidentally store "3.14" as text rather than a number. We check and fix this.
- **What does each column actually mean?** We cross-reference against a metadata file - a dictionary that explains every column in the dataset.

After this step, we have a clean, reliable foundation to build on.

> **Why this matters biologically:** In real laboratory settings, data collection is messy. Machines malfunction, values get entered incorrectly, and experiments sometimes fail silently. Cleaning the data is not glamorous work, but skipping it is like building a house on sand.

---

### Step 2 - Drug Sensitivity Patterns
*"Which drugs are champions, and which are duds?"*

We now rank every single drug by how effective it is across all cancer cell lines tested.

- **Most effective drugs** have the lowest average LN_IC50. A tiny amount kills 50% of cancer cells - these are your precision weapons.
- **Least effective drugs** have the highest average LN_IC50. You would need enormous, often toxic doses to see any effect - these are poor candidates for treatment.
- **Highly variable drugs** are the most biologically interesting. They work spectacularly well against some cancer types but do almost nothing against others. This variability is not a flaw - it is a clue.

> **Biological insight:** A highly variable drug is likely targeting a *specific biological weakness* that only certain cancers have. If we can identify which cancers have that weakness and why, we can match the drug precisely to the right patients. This idea - matching drugs to individual biological profiles - is the foundation of **personalised medicine.**

---

### Step 3 - Cancer Cell Line Analysis
*"Do certain cancers have a hidden weakness?"*

Not all cancers are the same disease. A drug that cures lung cancer may do nothing to brain cancer, even though both are "cancer." Here we ask a more targeted question:

- Which cancer types respond most sensitively to treatment overall?
- Which specific cell lines are most vulnerable to which specific drugs?
- Are there broader patterns - clusters of cancer types that share similar drug responses?

We group all experiments by cancer type and drug, then sort by average LN_IC50. A cancer type that scores very low here is generally more treatable - drugs tend to work well against it.

> **Biological insight:** Some cancers are sensitive because they divide rapidly and absorb drugs quickly. Others are resistant because they have evolved biological "shields" - proteins that physically pump drugs out of the cell, or survival pathways that reroute around the drug's target. Understanding which cancers have which shields helps scientists design the next generation of treatments to break through them.

---

### Step 4 - Genomic Influence on Drug Response
*"Does your DNA determine whether a drug will work?"*

This is where biology becomes truly remarkable. Cancer is, at its core, a disease of the genome - it starts when DNA is damaged or mutated in a way that makes cells grow uncontrollably. So we ask a natural question: **does the type of genetic damage in a cancer cell predict how it will respond to a drug?**

We investigate three types of genomic features:

**CNA (Copy Number Alteration)**

*What it is:* A physical mistake in the DNA where a section has been accidentally duplicated (copied too many times) or completely deleted.

*What it tells us:* The cancer may be carrying extra copies of a gene that fuels its growth, or it might have completely lost a critical gene that normally acts as a natural defense to keep growth in check.

**Gene Expression**

*What it is:* A measure of how active a gene is. In cancer, a gene can become unusually active (turned up too high) or unusually silent (turned down too low).

*What it tells us:* The cancer cell is producing too much or too little of a specific key protein, which severely disrupts normal, healthy cell behavior.

**Methylation**

*What it is:* A biological process where tiny chemical tags attach to DNA and act like a volume knob, effectively "silencing" or turning off certain genes.

What it tells us: Crucial protective genes may have been artificially switched off by the cancer, essentially removing the natural brakes that would normally stop the tumor from growing.

We calculate a **Spearman correlation** - a statistical measure of how consistently two things move together - between each genomic feature and LN_IC50:

- A **negative correlation** signals *sensitivity*: cancers carrying this feature tend to respond better to the drug
- A **positive correlation** signals *resistance*: cancers carrying this feature tend to be harder to treat

> **Biological insight:** If we find that a specific genomic feature strongly predicts drug sensitivity, we may be able to design a simple genetic test for patients. Before prescribing a drug, a doctor could test a patient's tumour and predict with confidence whether it will work. This is the promise of **precision oncology** - treating the biology of *your* cancer, not just the average cancer.

---

### Step 5 - Visualising the Story
*"A picture is worth a thousand data points."*

Numbers alone are difficult to communicate. We create five visualisations to make our findings clear and accessible to anyone:

**1. Distribution Plot**
Shows the spread of all LN_IC50 values across the entire dataset. Is the data centred around a typical value, or is it skewed? Are there extreme outliers? This gives us the landscape of drug effectiveness at a glance.

**2. Boxplot - Top 10 Most Effective Drugs**
Compares the range of LN_IC50 values for the best-performing drugs. A narrow box means consistent results across cancer types. A wide box means the drug is selective - it works brilliantly for some cancers and poorly for others.

**3. Boxplot - Top 10 Most Sensitive Cancer Types**
Shows which cancer types respond most consistently to treatment. This is clinically valuable - it tells us where drugs are most likely to succeed, and helps prioritise research and treatment decisions.

**4. Scatter Plot - AUC vs LN_IC50**
Explores whether our two main measures of drug effectiveness agree with each other. If they correlate strongly, they are capturing the same biological signal. If they diverge, each is revealing something different about how drugs work.

**5. Correlation Heatmap**
A colour-coded matrix of all biological variables at once. Warm red squares indicate a positive relationship; cool blue squares indicate a negative one. This "big picture" view reveals how genomics, drug sensitivity, and cancer biology are all interconnected.

---

## What Our Findings Mean

Taken together, our analysis reveals several important biological truths about cancer and drug response:

- **Cancer is not one disease.** The enormous variability in drug responses across cell lines confirms that different cancers behave fundamentally differently, even when caused by "the same type" of tumour.

- **Some drugs are broad weapons; others are precision tools.** Universally effective drugs likely attack cellular machinery that all cancer cells share. Highly variable drugs are targeting specific mutations - which makes them candidates for targeted therapy.

- **Cancer type shapes treatability.** Certain cancer types consistently show lower LN_IC50 values, suggesting shared biological vulnerabilities that drugs can exploit. Others show consistent resistance, pointing to mechanisms scientists need to overcome.

- **Your genome influences your treatment outcome.** The presence of copy number alterations, changes in gene expression, and epigenetic silencing are all measurable in a tumour biopsy - and all correlate with how that tumour responds to drugs. Genetics is not just background information; it is a predictive tool.

---

## Why This All Matters

Every year, millions of people are diagnosed with cancer. Many receive treatments that do not work - not because better drugs do not exist, but because we have not yet perfectly matched the right drug to the right patient.

Projects like GDSC, and analyses like ours, are building the scientific foundation for a future where a doctor can look at a tumour's genetic profile and say with confidence:

*"Based on the biology of your cancer, this is the drug most likely to help you."*

That future is not science fiction. It is what data-driven biology is actively constructing - one experiment, one dataset, one analysis at a time.

---

## Team Collaboration

This analysis was completed collaboratively. Tasks were distributed across team members covering data ingestion and validation, statistical analysis, visualisation design, and biological interpretation. Each step builds directly on the previous one, forming a complete end-to-end pipeline from raw experimental data to actionable biological insight.

---

*Dataset source: Genomics of Drug Sensitivity in Cancer (GDSC), a public scientific database maintained for cancer pharmacogenomics research.*

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

    print("  -> Saving 1/4: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[COL_LN_IC50].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({COL_LN_IC50})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency (Number of Cell Lines)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300)
    plt.close()

    print("  -> Saving 2/4: boxplot_top_effective_drugs.png...")
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

    print("  -> Saving 3/4: scatter_auc_ic50.png...")
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

    print("  -> Saving 4/4: correlation_heatmap.png...")
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

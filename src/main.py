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

    # Selectivity analysis: drugs with the most differential response across cancer types
    print("\n--- Drug Selectivity: Largest LN_IC50 spread across cancer types ---")
    if COL_CANCER_TYPE in df.columns and COL_DRUG in df.columns:
        drug_cancer_pivot = df.groupby([COL_DRUG, COL_CANCER_TYPE])[COL_LN_IC50].mean().unstack(COL_CANCER_TYPE)
        # Selectivity score = std dev of per-cancer-type mean LN_IC50
        selectivity = drug_cancer_pivot.std(axis=1).dropna().sort_values(ascending=False)
        print("Top 10 most selective drugs (work very differently across cancer types):")
        print(selectivity.head(10).to_frame('selectivity_score'))


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

    return correlations


def visualize_results(df):
    """Generate and save supporting visualizations for the GDSC dataset."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    print(f"\nGenerating Data Visualizations and saving to: {output_dir}")

    if COL_LN_IC50 not in df.columns:
        print(f"  -> Column '{COL_LN_IC50}' not found. Cannot generate visualizations.")
        return

    sns.set_theme(style="whitegrid")

    # 1/7: Distribution of LN_IC50
    print("  -> Saving 1/7: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[COL_LN_IC50].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({COL_LN_IC50})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300)
    plt.close()

    # 2/7: Boxplot — top 10 most effective drugs
    print("  -> Saving 2/7: boxplot_top_effective_drugs.png...")
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

    # 3/7: Boxplot — top 10 most sensitive cancer types
    print("  -> Saving 3/7: boxplot_cancer_types.png...")
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

    # 4/7: Scatter — AUC vs LN_IC50
    print("  -> Saving 4/7: scatter_auc_ic50.png...")
    if COL_AUC in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=COL_AUC, y=COL_LN_IC50, alpha=0.3, color='darkorange')
        plt.title(f'Relationship between {COL_AUC} and {COL_LN_IC50}', fontsize=14, fontweight='bold')
        plt.xlabel('AUC (Area Under the Curve)', fontsize=12)
        plt.ylabel(COL_LN_IC50, fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50.png"), dpi=300)
        plt.close()

    # 5/7: Correlation heatmap
    print("  -> Saving 5/7: correlation_heatmap.png...")
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

    # 6/7: Violin plots — LN_IC50 by genomic feature (Y vs N)
    print("  -> Saving 6/7: violin_genomic_features.png...")
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

    # 7/7: Pivot heatmap — top cancer types vs top drugs
    print("  -> Saving 7/7: heatmap_cancer_drug_pivot.png...")
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

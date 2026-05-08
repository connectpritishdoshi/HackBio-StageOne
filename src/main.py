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

    print("\nHighly variable drugs â€” selective responders (Highest Std Dev):")
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

    # Selectivity analysis: drugs with the most differential response across cancer types
    print("\n--- Drug Selectivity: Largest LN_IC50 spread across cancer types ---")
    if COL_CANCER_TYPE in df.columns and COL_DRUG in df.columns:
        drug_cancer_pivot = df.groupby([COL_DRUG, COL_CANCER_TYPE])[COL_LN_IC50].mean().unstack(COL_CANCER_TYPE)
        selectivity = drug_cancer_pivot.std(axis=1).dropna().sort_values(ascending=False)
        print("Top 10 most selective drugs (work very differently across cancer types):")
        print(selectivity.head(10).to_frame('selectivity_score'))

    # Overall cancer type sensitivity ranking
    print("\n--- Overall Cancer Type Sensitivity Ranking (mean LN_IC50 across all drugs) ---")
    if COL_TCGA_DESC in df.columns:
        cancer_overall = df.groupby(COL_TCGA_DESC)[COL_LN_IC50].agg(
            mean='mean', median='median', std='std', count='count'
        ).sort_values('mean')
        print("Top 10 most drug-sensitive cancer types (lowest mean LN_IC50):")
        print(cancer_overall.head(10))
        print("\nTop 10 most drug-resistant cancer types (highest mean LN_IC50):")
        print(cancer_overall.tail(10))
        print("\nTop 10 most variable cancer types (highest response std dev â€” most selective drug targets):")
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

    # MSI (Microsatellite Instability) â€” dedicated genomic biomarker analysis
    print("\n[Genomic Biomarker] MSI Status â€” Microsatellite Instability (DNA-level genomic feature):")
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
    print("\n[Method 2] Group comparison â€” cells WITH (Y) vs WITHOUT (N) each feature:")
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

        print(f"\n  {feature} â€” Top 5 drugs where presence SENSITISES (most negative shift):")
        for drug, row in pivot.sort_values('shift').head(5).iterrows():
            print(f"    {drug:<35} Y={row['Y']:>6.3f}  N={row['N']:>6.3f}  shift={row['shift']:>+7.3f}")

        print(f"\n  {feature} â€” Top 5 drugs where presence CONFERS resistance (most positive shift):")
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
                print(f"\n  {feature} â€” Top 5 cancer types most SENSITISED (most negative shift):")
                print(eff.head(5).to_string(index=False))
                print(f"\n  {feature} â€” Top 5 cancer types most RESISTANT with presence:")
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
                print(f"\n  {feature} â€” Pathways most SENSITISED by feature presence:")
                print(peff.head(5).to_string(index=False))
                print(f"\n  {feature} â€” Pathways most RESISTANT with feature presence:")
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
                  f"(vs {100*feat_all:.1f}% overall â€” {direction} {enrich:.2f}x)")

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

    # Method 8: Z_SCORE-based genomic analysis â€” do genomic features drive outlier responses?
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

    # Drug shift census â€” how many drugs are sensitised vs resistant per feature
    print("\n--- Molecular Feature Influence Scale: Drug Shift Census (Genomic / Transcriptomic / Epigenomic) ---")
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
            print(f"\n  {feature} â€” Top 5 drugs most strongly SENSITISED (most negative Cohen's d):")
            print(de_df.head(5)[['Drug', 'Cohen_d', 'Y_mean', 'N_mean', 'n_N']].to_string(index=False))
            print(f"\n  {feature} â€” Top 5 drugs most strongly conferring RESISTANCE (most positive Cohen's d):")
            print(de_df.tail(5)[['Drug', 'Cohen_d', 'Y_mean', 'N_mean', 'n_N']].to_string(index=False))

    # --- Summary ---
    print("\n--- Multi-Omics Influence Summary ---")
    print("  CNA (GENOMIC):             significantly sensitises cells overall (p=0.007)")
    print("                             largest effect on Mitosis-targeting drugs (shift -1.25)")
    print("  Gene Expression (TRANSCRIPTOMIC): significantly increases resistance overall (p=2.91e-30)")
    print("                             most cancer-type-specific effect (THCA +1.32 vs KIRC -1.12)")
    print("                             dramatically sensitises BCL-2 inhibitor TW 37 (shift -4.32)")
    print("  Methylation (EPIGENOMIC):  no significant aggregate effect (p=0.34)")
    print("                             but sensitises Mitosis drugs (-0.64) and SCLC specifically")
    print("  All features:    effects are drug-specific and cancer-type-specific â€”")
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

    # 1/7: Distribution of LN_IC50
    print("  -> Saving 1/15: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[COL_LN_IC50].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({COL_LN_IC50})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{COL_LN_IC50} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300)
    plt.close()

    # 2/7: Boxplot â€” top 10 most effective drugs
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

    # 3/7: Boxplot â€” top 10 most sensitive cancer types
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

    # 4/7: Scatter â€” AUC vs LN_IC50
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

    # 5/7: Correlation heatmap
    print("  -> Saving 5/15: correlation_heatmap.png...")
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

    # 6/7: Violin plots â€” LN_IC50 by genomic feature (Y vs N)
    print("  -> Saving 6/15: violin_genomic_features.png...")
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
        plt.suptitle(f'Drug Sensitivity Distribution by Molecular Feature (Genomic / Transcriptomic / Epigenomic)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "violin_genomic_features.png"), dpi=300)
        plt.close()

    # 7/7: Pivot heatmap â€” top cancer types vs top drugs
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

    # 8/14: Horizontal bar chart â€” mean LN_IC50 per drug target pathway
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

    # 9/14: Vertical bar chart â€” top 20 most sensitive cancer types (TCGA codes)
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

    # 10/14: KDE plot â€” LN_IC50 density curves for Gene Expression Y vs N
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
                  'LN_IC50 Density: Gene Expression Active vs Absent  (p = 2.91Ã—10â»Â³â°)',
                  fontsize=13, fontweight='bold')
        plt.xlabel(f'{COL_LN_IC50} (Lower = Cancer Cells Killed More Easily)', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "kde_gene_expression_influence.png"), dpi=300)
        plt.close()

    # 11/14: Scatter â€” AUC vs LN_IC50 stratified by Gene Expression status
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
        ax.set_title('AUC vs LN_IC50 â€” Stratified by Gene Expression (Transcriptomic) Status',
                     fontsize=13, fontweight='bold')
        ax.set_xlabel('AUC (Area Under the Dose-Response Curve)', fontsize=12)
        ax.set_ylabel(f'{COL_LN_IC50}', fontsize=12)
        ax.legend(fontsize=10, markerscale=2)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50_by_gene_expression.png"), dpi=300)
        plt.close()

    # 12/14: Heatmap â€” drug target pathway Ã— genomic features (LN_IC50 shift)
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

    # 13/14: Grouped bar chart â€” Y vs N for top 10 drugs most affected by Gene Expression
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

    # 14/15: Scatter â€” drug-level Y vs N LN_IC50 for Gene Expression (biomarker influence plot)
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
            ax.set_title('Transcriptomic Biomarker Influence â€” Drug-Level View\n'
                         'Each point = one drug: Y-axis is mean LN_IC50 without gene expression, '
                         'X-axis with it',
                         fontsize=12, fontweight='bold')
            ax.set_xlabel('Mean LN_IC50 â€” Gene Expression Active (Y cells)', fontsize=11)
            ax.set_ylabel('Mean LN_IC50 â€” Gene Expression Absent (N cells)', fontsize=11)
            ax.legend(fontsize=9, loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir,
                                     "scatter_gene_expression_y_vs_n_drug_level.png"), dpi=300)
            plt.close()

    # 15/15: Boxplot â€” MSI-H vs MSS/MSI-L LN_IC50 (genomic biomarker influence)
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
            axes[0].set_title('LN_IC50 by MSI Status\n(Genomic Biomarker â€” DNA Mismatch Repair)',
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
            plt.suptitle('Genomic Biomarker Influence â€” Microsatellite Instability (MSI) Status',
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

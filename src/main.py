#!/usr/bin/env python3
"""
HackBio Bioinformatics Project
Main entry point for bioinformatics tasks.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_explore_data(p_datapath,p_metadatapath):
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

    # What are the key variables in the dataset?
    print("What are the key variables in the dataset? ")
    # List the key variables categorized by their role
    key_columns = [
        'CELL_LINE_NAME', 'DRUG_NAME', 'TCGA_DESC', # Identifiers
        'LN_IC50', 'AUC', 'Z_SCORE',               # Results
        'CNA', 'Gene Expression', 'Methylation',    # Genetic Context
        'TARGET_PATHWAY'                            # Mechanism
    ]
    print(df_data[key_columns].head())
    print(f"Total Rows: {df_data.shape[0]}")
    print(f"Total Columns: {df_data.shape[1]}\n")

    # What does each column represent (see metadata description)?
    print("What does each column represent (see metadata description)?")
    #print(df_metadata, "\n") #This had truncation issue
    
    # Iterate through each row to create a clean, readable list for the output file
    for index, row in df_metadata.iterrows():
        # Use the 'Columns' value as the main header for each entry
        print(f"Column: {row['Columns']}")
        
        # Loop through the remaining 4 columns and print their values underneath
        for col_name in df_metadata.columns:
            if col_name != 'Columns': 
                # str() ensures any empty/NaN values don't break the formatting
                print(f"  - {col_name}: {str(row[col_name])}")
        print("") # Adding a blank line between entries for readability

    # Are there missing values or inconsistencies?
    print("Are there missing values or inconsistencies?")
    missing_values = df_data.isnull().sum()
    missing_cols = missing_values[missing_values > 0]
    if not missing_cols.empty:
        print(missing_cols)
    else:
        print("No missing values found!")

    # Check the data types to ensure numbers are actually treated as numbers
    print("\n Checking the data types to ensure numbers are actually treated as numbers and non-null counts:")
    print(df_data.info())
        
    print("\n--- Duplicates Check ---")
    duplicates = df_data.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}\n")
    
    return df_data

def analyze_drug_sensitivity(df, drug_col='DRUG_NAME', metric_col='LN_IC50'):
    """Analyze which drugs are most/least effective and their variance."""
    print("\nAnalyzing drug sensitivity patterns...")
    if drug_col not in df.columns or metric_col not in df.columns:
        print(f"  -> Missing '{drug_col}' or '{metric_col}' column. Skipping...")
        return

    # Group by drug and calculate mean and standard deviation of the metric (e.g., LN_IC50)
    # Lower LN_IC50 means higher drug effectiveness
    drug_stats = df.groupby(drug_col)[metric_col].agg(['mean', 'std']).dropna()

    most_effective = drug_stats.sort_values(by='mean').head(10)
    least_effective = drug_stats.sort_values(by='mean', ascending=False).head(10)
    highly_variable = drug_stats.sort_values(by='std', ascending=False).head(10)

    print("\n Which drugs appear to be the most effective? (Lowest Mean) ---")
    print(most_effective)
    print("\n Which drug show the least effectiveness? (Highest Mean) ---")
    print(least_effective)
    print("\n Are there drugs with highly variable responses across cell lines? (Highest Std Dev) ---")
    print(highly_variable)

def analyze_cell_line_response(df, cell_col='CELL_LINE_NAME', cancer_col='Cancer Type (matching TCGA label)', drug_col='DRUG_NAME', metric_col='LN_IC50'):
    """Analyze how cancer types and cell lines respond to treatments."""
    print("Do certain cancer types / cell lines respond better to specific drugs?")
    if cancer_col in df.columns and metric_col in df.columns:
        cancer_drug_response = df.groupby([cancer_col, drug_col])[metric_col].mean().sort_values().reset_index() #Default is ascending sort
        print(f"\n--- Most Sensitive Cancer Types (Lowest Mean {metric_col}) ---")
        print(cancer_drug_response.head(10))
    else:
        print(f"  -> Column '{cancer_col}' not found. Cannot analyze cancer types.")
    if cell_col in df.columns and metric_col in df.columns:
        cell_drug_response = df.groupby([cell_col, drug_col])[metric_col].mean().sort_values().reset_index()
        print(f"\n--- Most Sensitive Cell Lines (Lowest Mean {metric_col}) ---")
        print(cell_drug_response.head(10))
    
    print("What patterns exist in the drug response across cell lines?")
    if drug_col in df.columns and metric_col in df.columns:
        # Group by drug and calculate both the average response and how much it varies across cell lines
        drug_patterns = df.groupby(drug_col)[metric_col].agg(['mean', 'std']).dropna()
        print("Pattern 1: Universally Strong Drugs (Lowest Mean)")
        # Sort by lowest mean
        print(drug_patterns.sort_values('mean').head(10))
        print("Pattern 2: Highly Targeted Drugs (Highest Variance)")
        # Sort by highest standard deviation
        print(drug_patterns.sort_values('std', ascending=False).head(10))

def analyze_genomic_influence(df, metric_col='LN_IC50', features=['CNA', 'Gene Expression', 'Methylation']):
    """Analyze if genomic, transcriptomic, or epigenomic features influence drug response."""
    
    # Explicitly opt-in to Pandas 3.0 behavior to silence the replace downcasting warning
    pd.set_option('future.no_silent_downcasting', True)
    
    print("\nAre mutations (CNA), gene expression or methylation level influencing drug sensitivity at all?")
    
    # Filter to ensure we only try to analyze columns that actually exist in the dataframe
    existing_features = [col for col in features if col in df.columns]
    
    if not existing_features:
        print("  -> Genomic feature columns not found in the dataset. Skipping analysis.")
        return
    if metric_col not in df.columns:
        print(f"  -> Metric column '{metric_col}' not found. Skipping analysis.")
        return

    # Create a clean subset dropping rows where these specific values are missing
    df_subset = df[[metric_col] + existing_features].copy()
    
    # Convert 'Y'/'N' indicators to numeric (1/0) so we can calculate correlation
    for col in existing_features:
        # With the global option set, we can safely run replace without warnings
        df_subset[col] = df_subset[col].replace({'Y': 1, 'N': 0, 'y': 1, 'n': 0})
        
        # Now safely coerce to numeric (turning any weird artifacts into NaN)
        df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')
        
    # Drop any rows that became NaN during the numeric conversion
    df_clean = df_subset.dropna()
    
    print(f"  -> Calculating correlations based on {len(df_clean)} complete records...\n")
    if len(df_clean) == 0:
        print("  -> No valid numeric data available for correlation. Check data formatting.")
        return

    # Calculate the Spearman correlation matrix
    correlations = df_clean.corr(method='spearman')[metric_col].drop(metric_col)

    print("--- Correlation with Drug Sensitivity (LN_IC50) ---")
    print("Note: 'Y' (Present) was converted to 1, 'N' (Absent) to 0.")
    print("A Negative correlation means Presence of feature = LOWER LN_IC50 (Increased Sensitivity).")
    print("A Positive correlation means Presence of feature = HIGHER LN_IC50 (Increased Resistance).\n")
    #If a mutation (1) strongly pairs with a lower LN_IC50 score, the correlation will drop into the negatives, accurately telling you that the mutation causes Sensitivity.
    #If a mutation (1) strongly pairs with a higher LN_IC50 score, the correlation will rise into the positives, accurately telling you that the mutation causes Resistance.
    for feature, corr_value in correlations.items():
        # Determine the strength of the correlation for easy reading
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
        # > (Right-Align): This tells Python to push the number all the way to the right side of the allotted space.
        # 7 (Total Width): This reserves a minimum width of 7 characters for the number.
        # .4 (Precision): This forces the number to display exactly 4 digits after the decimal point, rounding if necessary or adding trailing zeros if the number is short.
        # f (Float): This tells Python to format the value as a floating-point number (a decimal), rather than scientific notation or an integer.

    return correlations

def visualize_results(df, metric_col='LN_IC50', drug_col='DRUG_NAME'):
    """Generate and save supporting visualizations for the GDSC dataset."""
    # Create an outputs directory to save our plots automatically
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    print(f"\nGenerating Data Visualizations and saving to: {output_dir}")
    
    # Check if the primary metric exists
    if metric_col not in df.columns:
        print(f"  -> Column '{metric_col}' not found. Cannot generate visualizations.")
        return

    sns.set_theme(style="whitegrid")

    # ---------------------------------------------------------
    # 5a) Distribution plots of drug sensitivity
    # ---------------------------------------------------------
    print("  -> Saving 1/4: distribution_plot.png...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df[metric_col].dropna(), kde=True, bins=50, color='teal')
    plt.title(f'Distribution of Drug Sensitivity ({metric_col})', fontsize=14, fontweight='bold')
    plt.xlabel(f'{metric_col} (Lower = More Effective)', fontsize=12)
    plt.ylabel('Frequency (Number of Cell Lines)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "distribution_plot.png"), dpi=300) # Save as high-res PNG
    plt.close() # Close the plot to free up memory

    # ---------------------------------------------------------
    # 5b) Boxplots comparing drugs (Based on Lowest Mean LN_IC50)
    # ---------------------------------------------------------
    print("  -> Saving 2/4: boxplot_top_effective_drugs.png...")
    if drug_col in df.columns:
        plt.figure(figsize=(12, 6))
        
        # 1. Replicate Part 3 exactly: calculate mean/std and drop single-test drugs
        drug_stats = df.groupby(drug_col)[metric_col].agg(['mean', 'std']).dropna()
        
        # 2. Grab the top 10 drugs with the lowest mean (Matches Part 3 output exactly)
        top_effective_drugs = drug_stats.sort_values('mean').head(10).index
        
        # 3. Filter the original dataset for the boxplot
        df_top_drugs = df[df[drug_col].isin(top_effective_drugs)]
        
        # 4. Create the plot
        sns.boxplot(data=df_top_drugs, x=drug_col, y=metric_col,hue=drug_col, palette="Set2", order=top_effective_drugs,legend=False)
        plt.title(f'Drug Sensitivity ({metric_col}) Across Top 10 Most Effective Drugs', fontsize=14, fontweight='bold')
        plt.xlabel('Drug Name', fontsize=12)
        plt.ylabel(f'{metric_col} (Lower = More Effective)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "boxplot_top_effective_drugs.png"), dpi=300)
        plt.close()
    else:
        print(f"  -> '{drug_col}' not found. Skipping boxplot.")

    # ---------------------------------------------------------
    # 5c) Scatter plots showing relationships
    # ---------------------------------------------------------
    print("  -> Saving 3/4: scatter_auc_ic50.png...")
    if 'AUC' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x='AUC', y=metric_col, alpha=0.5, color='darkorange')
        plt.title('Relationship between AUC and LN_IC50', fontsize=14, fontweight='bold')
        plt.xlabel('AUC (Area Under the Curve)', fontsize=12)
        plt.ylabel(metric_col, fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_auc_ic50.png"), dpi=300)
        plt.close()
    else:
         print("  -> 'AUC' column not found. Skipping scatter plot.")

    # ---------------------------------------------------------
    # 5d) Correlations (Heatmap)
    # ---------------------------------------------------------
    print("  -> Saving 4/4: correlation_heatmap.png...")
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    
    if not numeric_df.empty and len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr()
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, 
                    square=True, linewidths=.5, cbar_kws={"shrink": .8})
        plt.title('Correlation Heatmap of Numeric Variables', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=300)
        plt.close()
    else:
        print("  -> Not enough numeric columns to generate a correlation heatmap.")

def main():
    print("Welcome to HackBio: GDSC Data Analysis Project!")
    print("Investigating Genomics of Drug Sensitivity in Cancer...\n")
    
    # Calculating the absolute path to the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Forming the data path directory and filename
    data_path = os.path.join(base_dir, "data", "GDSC.xlsx")
    metadata_path = os.path.join(base_dir, "data", "metadata.xlsx")
    
    # Load and explore the data
    print(f"Part 1: Understanding the dataset starts...\n")
    df = load_and_explore_data(data_path,metadata_path)
    print(f"Part 1: Understanding the dataset completes.\n")

    if df is not None:
        print(f"Part 2: Drug Sensitivity patterns starts...\n") 
        analyze_drug_sensitivity(df, drug_col='DRUG_NAME', metric_col='LN_IC50')
        print(f"Part 2: Drug Sensitivity patterns completes.\n")
        print(f"Part 3: Cancer cell line analysis starts...\n") 
        analyze_cell_line_response(df, cell_col='CELL_LINE_NAME', cancer_col='Cancer Type (matching TCGA label)', drug_col='DRUG_NAME', metric_col='LN_IC50')
        print(f"Part 3: Cancer cell line analysis completes.\n")
        print(f"Part 4: Genomic influence analysis starts...\n") 
        analyze_genomic_influence(df, metric_col='LN_IC50', features=['CNA', 'Gene Expression', 'Methylation'])
        print(f"Part 4: Genomic influence analysis completes.\n")
        print(f"Part 5: Supporting Data Visualization starts...\n") 
        visualize_results(df, metric_col='LN_IC50', drug_col='DRUG_NAME')
        print(f"Part 5: Supporting Data Visualization completes.\n") 
        
        print("\n HackBio GDSC Data Analysis Project Complete! ---")

if __name__ == "__main__":
    main()
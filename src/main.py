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
    print(df_metadata, "\n")

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


if __name__ == "__main__":
    main()
"""
Gulf of Mexico (GoM) OGOR-A Regulatory Production ETL Pipeline
Author: Pritam Kundu
Description: Ingests, normalizes, and consolidates multi-file raw OGOR-A 
             production text feeds into an analytics-ready dataset.
"""

import glob
import os
import pandas as pd

# 19-column schema definition based on BOEM / BSEE OGOR-A file layout
OGORA_COLUMNS = [
    "LEASE_NUM",        # Col 1: Mineral lease identifier
    "WELL_NAME",        # Col 2: Well identification name
    "PROD_DATE",        # Col 3: Production period (YYYYMM)
    "DAYS_PRODUCED",    # Col 4: Operational producing days in month
    "PROD_CODE",        # Col 5: Product disposition code
    "OIL_PROD",         # Col 6: Monthly oil production volume (BBL)
    "GAS_PROD",         # Col 7: Monthly gas production volume (MCF)
    "WATER_PROD",       # Col 8: Monthly water production volume (BBL)
    "API_WELL_NUM",     # Col 9: Unique 10-12 digit API wellbore identifier
    "STATUS_CODE",      # Col 10: Well status code
    "AREA_BLOCK",       # Col 11: OCS block area descriptor
    "OPERATOR_NUM",     # Col 12: Unique operator company number
    "OPERATOR_NAME",    # Col 13: Operating entity company name
    "FIELD_NAME",       # Col 14: Subsurface field designation
    "PRESSURE_METRIC",  # Col 15: Wellhead tubing/casing pressure metric
    "COMPLETION_CODE",  # Col 16: Well completion interval code
    "FIRST_PROD_DATE",  # Col 17: Date of initial commercial production
    "EXTRA_1",          # Col 18: Reserved regulatory field 1
    "EXTRA_2",          # Col 19: Reserved regulatory field 2
]

# Primary string fields requiring whitespace removal and text sanitization
STRING_COLUMNS = [
    "LEASE_NUM",
    "WELL_NAME",
    "API_WELL_NUM",
    "OPERATOR_NUM",
    "OPERATOR_NAME",
    "PROD_DATE",
]

# Numeric measurements requiring type casting and missing-value handling
NUMERIC_COLUMNS = [
    "DAYS_PRODUCED",
    "OIL_PROD",
    "GAS_PROD",
    "WATER_PROD",
    "PRESSURE_METRIC",
]


def load_and_clean_ogor_file(file_path: str) -> pd.DataFrame:
    """
    Ingests an individual raw comma-separated text file, applies the fixed
    19-column schema, strips whitespace, and skips malformed records.
    """
    df = pd.read_csv(
        file_path,
        sep=",",
        header=None,
        names=OGORA_COLUMNS,
        dtype=str,
        skipinitialspace=True,
        on_bad_lines="skip",
    )

    # Sanitize string attributes
    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


def run_pipeline():
    # 1. Discover all raw OGOR text feeds in directory
    raw_files = sorted(
        [
            f
            for f in glob.glob("ogora*.txt")
            if os.path.isfile(f) and not f.endswith(("_clean.csv", "production.csv"))
        ]
    )

    if not raw_files:
        print("No raw OGOR text files found matching pattern 'ogora*.txt'.")
        return

    print(f"Discovered {len(raw_files)} raw files to process: {raw_files}")

    # 2. Batch ingestion and concatenation
    dfs = [load_and_clean_ogor_file(f) for f in raw_files]
    final_df = pd.concat(dfs, ignore_index=True)

    # 3. Numeric type casting and null imputation
    for col in NUMERIC_COLUMNS:
        final_df[col] = pd.to_numeric(final_df[col], errors="coerce").fillna(0)

    # 4. Export consolidated output
    output_filename = "merged_ogora_production.csv"
    final_df.to_csv(output_filename, index=False)
    print(f"ETL Complete: Saved {len(final_df):,} records to {output_filename}")


if __name__ == "__main__":
    run_pipeline()

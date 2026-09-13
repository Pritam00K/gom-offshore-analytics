# Gulf of Mexico (GoM) Offshore Commercial & Asset Analytics Platform

## Executive Summary
An enterprise-grade production analytics and asset degradation monitoring framework evaluating **223,000+ monthly production records** and **55,500+ unique wellbores** across the Gulf of Mexico Outer Continental Shelf (OCS). The platform pairs an automated Python ETL pipeline for multi-source regulatory data aggregation with a relational Power BI engine for geospatial tracking and capital efficiency benchmarking.

## Architecture & Data Pipeline
```text
[ Raw BOEM / BSEE Regulatory Fixed-Width Text Files (19 Columns) ]
                            │
                            ▼
              [ Python Automated ETL (pandas) ]
  • Delimiter normalization & whitespace trimming
  • Header alignment & multi-file parsing
  • Datatype casting & null-value imputation
                            │
                            ▼
           [ Staged Clean Tabular Dataset (Parquet/CSV) ]
                            │
                            ▼
          [ Power BI Relational Star Schema Model ]
  • Central Fact Table: Monthly Production Metrics (Oil, Gas, Water)
  • Dimension Tables: Wellbore Master, Operator Dimension, Date Dimension
                            │
                            ▼
               [ DAX Measure Calculation Engine ]
  • Dynamic GOR (Gas-to-Oil Ratio) formulation
  • Reservoir depletion tracking & YoY output variances
  • Water-cut threshold alerts (80%+ economic risk line)
                            │
                            ▼
         [ Executive Geospatial & Financial Dashboard ]
  • Basin-scale asset clustering via Azure Maps (Lat/Long)
  • Operator efficiency index (BOE per active wellbore)
```

## Key Technical Implementations

### 1. Data Cleansing & Automated ETL Pipeline (Python / pandas)
* **Data Harmonization:** Processed fixed-width, unformatted regulatory text feeds with 19 columns, resolving inconsistent spacing and string truncations into standardized tabular formats.
* **Scale & Volume:** Aggregated and cleansed 223,000+ monthly records covering 55,500+ historical wellbores into structured analytics-ready tables.
* **Integrity Validation:** Audited null values, formatted API well numbers, and cast temporal timestamps to ensure zero data loss during upstream ingestion.

### 2. Analytical Modeling & DAX Business Logic (Power BI)
* **Star Schema Architecture:** Designed a 1-to-many dimensional model linking 2,000 active production wellbores to operator and temporal hierarchies.
* **Maturity & Depletion Diagnostics:** Formulated DAX calculations tracking Gas-to-Oil Ratios (GOR) alongside water-cut escalation curves to diagnose late-life reservoir depletion.
* **Risk Threshold Flagging:** Visualized an **80% water disposal risk threshold** to flag sub-economic well clusters nearing operational shut-in status.
* **Macro Basin Trends:** Monitored YoY shifts in total barrel of oil equivalent (**212M+ BOE**) output against a 1.2% decline in drilling activity, evaluating aggregate basin extraction efficiency.

### 3. Geospatial Mapping & Operator Benchmarking
* **Geospatial Intelligence:** Integrated **Azure Maps** using explicit latitude/longitude coordinates to map wellbore density and spatial production distribution across offshore protraction areas.
* **Operator Efficiency Analysis:** Established a baseline performance index (1.11M BOE/well) to compare output metrics between high-volume legacy operators (Shell, BP) and mid-cap producers.

## Repository File Structure
```text
├── etl/
│   └── gom_data_pipeline.py          # Python script for text ingestion, cleaning & transformation
├── power_bi/
│   └── GoM_Offshore_Analytics.pbix    # Interactive Power BI dashboard report
└── README.md                         # Project documentation and architecture
```

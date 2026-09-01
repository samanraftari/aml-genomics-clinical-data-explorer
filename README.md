# AML Genomics & Clinical Data Explorer

A reproducible Python project exploring mutation patterns and clinical characteristics in acute myeloid leukemia (AML) using open-access, de-identified data from TCGA-LAML.

## Project status

This project is under active development. The first milestone is a transparent exploratory analysis that can be understood and reproduced before any machine-learning model is added.

## Questions

- Which genes are most frequently mutated in this AML cohort?
- How do mutation patterns vary across available clinical groups?
- Are selected molecular features associated with age or survival outcomes?
- What limitations must be considered when interpreting these associations?

## Planned workflow

1. Document and download permitted open-access data.
2. Validate patient identifiers, missingness, and variable definitions.
3. Clean and join clinical and mutation tables with Python.
4. Perform exploratory analysis and create publication-style figures.
5. Add statistical comparisons with clearly stated assumptions.
6. Consider an interpretable model only if the data support it.

## Repository structure

```text
aml-genomics-clinical-data-explorer/
├── data/
│   ├── raw/            # Original data; not committed unless redistribution is permitted
│   └── processed/      # Reproducible analysis-ready outputs
├── notebooks/          # Step-by-step exploratory notebooks
├── reports/figures/    # Exported figures
├── src/                # Reusable Python functions
├── .gitignore
├── README.md
└── requirements.txt
```

## Data source

The intended source is the open-access TCGA Acute Myeloid Leukemia cohort available through the NCI Genomic Data Commons and cBioPortal. Exact study identifiers, downloaded files, access date, and citation details will be recorded before analysis.

- NCI TCGA: https://www.cancer.gov/ccg/research/genome-sequencing/tcga
- GDC Data Portal: https://portal.gdc.cancer.gov/
- cBioPortal datasets: https://www.cbioportal.org/datasets

No private patient records or personally identifiable information will be used.

## Tools

- Python
- pandas and NumPy
- Matplotlib and Seaborn
- Jupyter
- SciPy and scikit-learn (only when analytically appropriate)

## Responsible interpretation

This is an educational portfolio project, not a clinical decision-support tool. Results will be exploratory, dataset-specific, and unsuitable for diagnosis, prognosis, or treatment decisions.

## Author

Saman Raftari  
Molecular genetics and clinical diagnostics professional developing skills in Python, bioinformatics, machine learning, and healthcare data analysis.

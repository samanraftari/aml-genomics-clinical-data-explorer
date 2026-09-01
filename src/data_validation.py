"""Data-validation helpers for AML clinical and genomic tables."""

import pandas as pd


def summarize_missingness(data: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages for each column."""
    summary = pd.DataFrame(
        {
            "missing_count": data.isna().sum(),
            "missing_percent": data.isna().mean().mul(100).round(2),
        }
    )
    return summary.sort_values("missing_percent", ascending=False)

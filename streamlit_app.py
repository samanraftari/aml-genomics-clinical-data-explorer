from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="AML Genomics & Clinical Data Explorer",
    page_icon="🧬",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
TABLE_DIR = ROOT / "reports" / "tables"
FIGURE_DIR = ROOT / "reports" / "figures"


@st.cache_data
def load_aggregate_results():
    """Load public, non-identifying aggregate results committed to the repository."""
    genes = pd.read_csv(TABLE_DIR / "top_15_mutated_genes.csv")
    variants = pd.read_csv(TABLE_DIR / "variant_classification_counts.csv")
    return genes, variants


top_genes, variant_classes = load_aggregate_results()

st.markdown(
    """
    <style>
    .block-container {max-width: 1200px; padding-top: 2rem;}
    [data-testid="stMetric"] {
        background: #f4f8f5;
        border: 1px solid #c8ddd2;
        border-radius: 14px;
        padding: 16px;
    }
    .hero {
        background: linear-gradient(135deg, #0b2942 0%, #134e5e 100%);
        border-radius: 20px;
        color: white;
        padding: 30px 34px;
        margin-bottom: 22px;
    }
    .hero h1 {margin: 0 0 8px; font-size: 2.25rem;}
    .hero p {margin: 0; color: #d8ece4; font-size: 1.05rem;}
    .note {
        border-left: 4px solid #168b7d;
        background: #f1f8f5;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
    }
    </style>
    <div class="hero">
      <h1>AML Genomics &amp; Clinical Data Explorer</h1>
      <p>Reproducible analysis of open-access, de-identified TCGA-LAML PanCancer Atlas data</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Study: laml_tcga_pan_can_atlas_2018 · Accessed September 1, 2026")

overview_tab, genes_tab, variants_tab, quality_tab, methods_tab = st.tabs(
    ["Overview", "Mutated genes", "Variant classes", "Data quality", "Methods & use"]
)

with overview_tab:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Patients", "200")
    c2.metric("Primary samples", "200")
    c3.metric("Validated somatic rows", "2,528")
    c4.metric("Samples with somatic variants", "197")

    st.subheader("What this project demonstrates")
    st.write(
        "A transparent Python workflow for validating linked clinical and genomic tables, "
        "assessing missingness, filtering explicitly labelled somatic mutations, and "
        "summarizing mutation patterns without publishing raw patient-level records."
    )

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Leading altered genes")
        st.dataframe(
            top_genes.head(5).rename(
                columns={
                    "gene": "Gene",
                    "altered_samples": "Altered samples",
                    "frequency_percent": "Frequency (%)",
                }
            ),
            hide_index=True,
            use_container_width=True,
        )
    with right:
        st.subheader("Responsible interpretation")
        st.markdown(
            """
            <div class="note">
            Educational and exploratory only. This dashboard is not a diagnostic,
            prognostic, or treatment-selection tool. Findings are cohort-specific
            and require external validation.
            </div>
            """,
            unsafe_allow_html=True,
        )

with genes_tab:
    st.subheader("Most frequently mutated genes")
    st.write(
        "Frequency is the percentage of 200 profiled samples with at least one "
        "validated somatic mutation in the gene. Unique samples—not mutation rows—are counted."
    )

    gene_chart = (
        alt.Chart(top_genes)
        .mark_bar(color="#176b87", cornerRadiusEnd=4)
        .encode(
            x=alt.X("frequency_percent:Q", title="Samples with mutation (%)"),
            y=alt.Y("gene:N", sort="-x", title=None),
            tooltip=[
                alt.Tooltip("gene:N", title="Gene"),
                alt.Tooltip("altered_samples:Q", title="Altered samples"),
                alt.Tooltip("frequency_percent:Q", title="Frequency", format=".1f"),
            ],
        )
        .properties(height=480)
    )
    st.altair_chart(gene_chart, use_container_width=True)
    st.dataframe(top_genes, hide_index=True, use_container_width=True)

with variants_tab:
    st.subheader("Variant classification landscape")
    st.write(
        "Counts describe validated somatic records in this export. A reported variant "
        "classification does not by itself establish clinical actionability."
    )

    variant_chart = (
        alt.Chart(variant_classes)
        .mark_bar(color="#2a9d8f", cornerRadiusEnd=4)
        .encode(
            x=alt.X("variant_count:Q", title="Reported variants"),
            y=alt.Y("variant_classification:N", sort="-x", title=None),
            tooltip=[
                alt.Tooltip("variant_classification:N", title="Classification"),
                alt.Tooltip("variant_count:Q", title="Count"),
            ],
        )
        .properties(height=480)
    )
    st.altair_chart(variant_chart, use_container_width=True)

with quality_tab:
    st.subheader("Clinical-data quality findings")
    q1, q2, q3 = st.columns(3)
    q1.metric("Duplicate patient rows", "0")
    q2.metric("Duplicate sample rows", "0")
    q3.metric("Mutation-to-sample linkage", "100%")

    st.warning(
        "AGE and SEX are entirely missing in this cBioPortal clinical export. "
        "They are not imputed or used for downstream comparisons."
    )
    st.subheader("Reported mutation rows per sample")
    st.write(
        "This is a descriptive row count—not a standardized clinical tumor mutational burden. "
        "The display is capped at the 95th percentile to prevent extreme values from obscuring the distribution."
    )
    burden_figure = FIGURE_DIR / "reported_mutations_per_sample.png"
    if burden_figure.exists():
        st.image(str(burden_figure), use_container_width=True)

with methods_tab:
    st.subheader("Analysis workflow")
    st.markdown(
        """
        1. Load cBioPortal tab-separated clinical, sample, and mutation tables.
        2. Validate unique cohort keys and sample linkage.
        3. Quantify missingness before analysis.
        4. Retain records explicitly labelled `Mutation_Status = Somatic`.
        5. Calculate gene frequency using unique altered samples.
        6. Publish only aggregate tables, figures, code, and documentation.
        """
    )
    st.subheader("Data and privacy")
    st.write(
        "Only open-access, de-identified TCGA data are used. Raw patient-level source "
        "files are excluded from the public repository, and no re-identification is attempted."
    )
    st.link_button(
        "View reproducible notebook",
        "https://github.com/SamanRaftari/aml-genomics-clinical-data-explorer/blob/main/notebooks/01_aml_data_quality_and_mutation_landscape.ipynb",
    )
    st.link_button(
        "View GitHub repository",
        "https://github.com/SamanRaftari/aml-genomics-clinical-data-explorer",
    )

st.divider()
st.caption(
    "Created by Saman Raftari · Molecular genetics, clinical diagnostics, and developing bioinformatics skills"
)

import streamlit as st
import pandas as pd

from utils import (
    load_csv,
    validate_measures
)

from pivot import render_pivot
from charts import render_charts

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart CSV Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart CSV Analyzer")

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Carica CSV",
    type=["csv"]
)

if not uploaded_file:

    st.info("👆 Carica un CSV")

    st.stop()

# =========================
# LOAD DATA
# =========================
try:

    df = load_csv(uploaded_file)

except Exception as e:

    st.error(f"Errore CSV: {e}")

    st.stop()

# =========================
# DATAFRAME
# =========================
st.subheader("📄 Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# =========================
# COLUMN TYPES
# =========================
num_cols = df.select_dtypes(
    include="number"
).columns.tolist()

cat_cols = df.select_dtypes(
    exclude="number"
).columns.tolist()

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.header("⚙️ Controlli")

    dimensioni = st.multiselect(
        "Dimensioni",
        cat_cols
    )

    misure = st.multiselect(
        "Misure",
        num_cols
    )

    agg_func = st.selectbox(
        "Aggregazione",
        ["sum", "mean", "count"]
    )

    sort_order = st.radio(
        "Direzione ordinamento",
        ["Crescente", "Decrescente"]
    )

    # FILTRI
    st.subheader("🔎 Filtri")

    filtri = {}

    for col in dimensioni:

        valori = (
            df[col]
            .dropna()
            .unique()
            .tolist()
        )

        filtri[col] = st.multiselect(
            f"Filtra {col}",
            valori,
            default=valori
        )

# =========================
# FILTER DATA
# =========================
mask = pd.Series(
    True,
    index=df.index
)

for col, vals in filtri.items():

    if vals:

        mask &= df[col].isin(vals)

df_filtered = df[mask]

# =========================
# VALIDATE MEASURES
# =========================
if misure:

    df_filtered = validate_measures(
        df_filtered,
        misure
    )

# =========================
# MAIN APP
# =========================
if dimensioni and misure:
    st.divider()
    render_pivot(
        df_filtered,
        dimensioni,
        misure,
        agg_func,
        sort_order
    )
    st.divider()
    render_charts(
        df_filtered,
        dimensioni,
        misure
    )

else:

    st.info(
        "👉 Seleziona almeno una dimensione e una misura"
    )
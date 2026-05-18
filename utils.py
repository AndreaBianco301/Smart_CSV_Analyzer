import pandas as pd
import streamlit as st

# =========================
# LOAD CSV
# =========================
@st.cache_data
def load_csv(file):

    df = pd.read_csv(
        file,
        sep=";",
        engine="python"
    )

    return df.reset_index(drop=True)

# =========================
# SORT DATAFRAME
# =========================
def sort_dataframe(df, sort_col, ascending=True):

    return df.sort_values(
        by=sort_col,
        ascending=ascending
    )

# =========================
# AGGREGATION
# =========================
@st.cache_data
def aggregate_data(df, dimensions, measures, agg_func):

    if agg_func == "count":

        return (
            df.groupby(dimensions)
            .size()
            .reset_index(name="count")
        )

    return (
        df.groupby(dimensions)[measures]
        .agg(agg_func)
        .reset_index()
    )

# =========================
# VALIDATE MEASURES
# =========================
def validate_measures(df, measures):

    df = df.copy()

    for col in measures:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df.dropna(subset=measures)
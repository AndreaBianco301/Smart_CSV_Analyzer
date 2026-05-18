import streamlit as st
from utils import aggregate_data, sort_dataframe

# =========================
# RENDER PIVOT
# =========================
def render_pivot(df_filtered, dimensioni, misure, agg_func, sort_order):

    pivot = aggregate_data(
        df_filtered,
        dimensioni,
        misure,
        agg_func
    )

    st.subheader("📊 Pivot")

    sort_col = st.selectbox(
        "Ordina pivot per",
        pivot.columns.tolist(),
        key="pivot_sort"
    )

    ascending = (sort_order == "Crescente")

    pivot = sort_dataframe(
        pivot,
        sort_col,
        ascending
    )

    st.dataframe(
        pivot,
        use_container_width=True
    )

    return pivot
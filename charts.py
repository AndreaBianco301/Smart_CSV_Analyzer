import streamlit as st
import plotly.express as px

from utils import (
    aggregate_data,
    sort_dataframe
)

# =========================
# GRAFICI
# =========================
def render_charts(df_filtered, dimensioni, misure):

    st.subheader("📈 Grafici")

    if "charts" not in st.session_state:
        st.session_state.charts = []

    # =========================
    # ADD CHART
    # =========================
    if st.button("➕ Aggiungi grafico"):

        st.session_state.charts.append(True)

        st.rerun()

    # =========================
    # LOOP CHARTS
    # =========================
    charts_to_remove = []

    for i in range(len(st.session_state.charts)):

        with st.expander(
            f"📈 Grafico {i+1}",
            expanded=True
        ):

            # REMOVE
            if st.button(
                "🗑️ Elimina",
                key=f"remove_{i}"
            ):

                charts_to_remove.append(i)

            # CONTROLS
            x_col = st.selectbox(
                "Dimensione (X)",
                dimensioni,
                key=f"x_{i}",
                index = 0
            )

            y_cols = st.multiselect(
                "Misure (Y)",
                misure,
                key=f"y_{i}",
                default=[misure[0]] if misure else []
            )

            chart_type = st.selectbox(
                "Tipo grafico",
                ["Bar", "Line"],
                key=f"type_{i}"
            )

            agg_func = st.selectbox(
                "Aggregazione",
                ["sum", "mean", "count"],
                key=f"agg_{i}"
            )

            sort_col = st.selectbox(
                "Ordina per",
                [x_col] + y_cols if y_cols else [x_col],
                key=f"sort_{i}"
            )

            sort_dir = st.radio(
                "Direzione",
                ["Crescente", "Decrescente"],
                key=f"dir_{i}"
            )

            # =========================
            # BUILD CHART
            # =========================
            if x_col and y_cols:

                df_chart = aggregate_data(
                    df_filtered,
                    [x_col],
                    y_cols,
                    agg_func
                )

                ascending = (
                    sort_dir == "Crescente"
                )

                df_chart = sort_dataframe(
                    df_chart,
                    sort_col,
                    ascending
                )

                # LONG FORMAT
                df_long = df_chart.melt(
                    id_vars=x_col,
                    value_vars=y_cols,
                    var_name="Misura",
                    value_name="Valore"
                )

                # LINE
                if chart_type == "Line":

                    fig = px.line(
                        df_long,
                        x=x_col,
                        y="Valore",
                        color="Misura",
                        markers=True
                    )

                # BAR
                else:

                    fig = px.bar(
                        df_long,
                        x=x_col,
                        y="Valore",
                        color="Misura",
                        barmode="group"
                    )

                fig.update_layout(
                    height=500,
                    hovermode="x unified",
                    xaxis_tickangle=-90
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"plotly_chart_{i}"
                )

    # REMOVE CHARTS
    if charts_to_remove:

        for i in reversed(charts_to_remove):

            st.session_state.charts.pop(i)

        st.rerun()
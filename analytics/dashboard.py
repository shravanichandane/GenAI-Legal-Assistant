"""
Module 12: Analytics Layer
Provides a Streamlit dashboard for visualizing metrics and insights.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(metrics_data: dict):
    """
    Renders the analytics dashboard using Streamlit.
    """
    st.title("Analytics Dashboard")
    st.markdown("Visualize the performance and metrics of the system.")

    if not metrics_data:
        st.warning("No metrics data available.")
        return

    # Basic KPI metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Documents Processed", metrics_data.get("total_docs", 0))
    col2.metric("Average Processing Time (s)", round(metrics_data.get("avg_processing_time", 0.0), 2))
    col3.metric("Overall Accuracy", f"{metrics_data.get('overall_accuracy', 0.0) * 100:.1f}%")

    st.subheader("Performance Over Time")
    history = metrics_data.get("history", [])
    if history:
        df = pd.DataFrame(history)
        fig = px.line(df, x="timestamp", y="accuracy", title="Accuracy Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No historical data available to plot.")

    st.subheader("Error Distribution")
    errors = metrics_data.get("errors", {})
    if errors:
        error_df = pd.DataFrame(list(errors.items()), columns=["Error Type", "Count"])
        fig2 = px.pie(error_df, values="Count", names="Error Type", title="Error Types")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No error data available.")

if __name__ == "__main__":
    # Dummy data for testing the dashboard
    dummy_data = {
        "total_docs": 1250,
        "avg_processing_time": 1.45,
        "overall_accuracy": 0.94,
        "history": [
            {"timestamp": "2023-01-01", "accuracy": 0.90},
            {"timestamp": "2023-01-02", "accuracy": 0.92},
            {"timestamp": "2023-01-03", "accuracy": 0.91},
            {"timestamp": "2023-01-04", "accuracy": 0.95},
        ],
        "errors": {
            "Timeout": 12,
            "Parse Error": 5,
            "Missing Value": 8
        }
    }
    render_dashboard(dummy_data)

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json


def generate_chart(df: pd.DataFrame, chart_type: str = "auto", x_col: str | None = None, y_col: str | None = None) -> dict:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    if chart_type == "auto":
        if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            chart_type = "bar"
        elif len(numeric_cols) >= 2:
            chart_type = "scatter"
        elif len(numeric_cols) >= 1:
            chart_type = "histogram"
        else:
            chart_type = "bar"

    if chart_type == "line":
        x = x_col or categorical_cols[0] if categorical_cols else df.index
        y = y_col or numeric_cols[0] if numeric_cols else df.columns[0]
        fig = px.line(df, x=x, y=y, title="Line Chart")
    elif chart_type == "bar":
        x = x_col or categorical_cols[0] if categorical_cols else df.index
        y = y_col or numeric_cols[0] if numeric_cols else df.columns[0]
        fig = px.bar(df, x=x, y=y, title="Bar Chart")
    elif chart_type == "histogram":
        col = x_col or numeric_cols[0] if numeric_cols else df.columns[0]
        fig = px.histogram(df, x=col, title="Histogram")
    elif chart_type == "heatmap" and len(numeric_cols) >= 2:
        fig = px.imshow(df[numeric_cols].corr(), text_auto=True, title="Correlation Heatmap")
    else:
        x = x_col or categorical_cols[0] if categorical_cols else df.index
        y = y_col or numeric_cols[0] if numeric_cols else df.columns[0]
        fig = px.bar(df, x=x, y=y, title="Bar Chart")

    fig_json = json.loads(fig.to_json())
    return {
        "chart_type": chart_type,
        "data": fig_json,
    }

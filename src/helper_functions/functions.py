"""
Basic Helper Functions for Quarto Data Analysis

Simple utility functions to get you started with data analysis in Quarto.
These functions provide basic data manipulation and visualization helpers.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from typing import Dict, Any


def load_sample_data(n_rows: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate sample data for testing and demonstrations.

    Args:
        n_rows: Number of rows to generate
        seed: Random seed for reproducibility

    Returns:
        pandas DataFrame with sample data
    """
    np.random.seed(seed)

    dates = pd.date_range(start="2023-01-01", periods=n_rows, freq="D")

    data = {
        "date": np.random.choice(dates, n_rows),
        "category": np.random.choice(
            ["A", "B", "C", "D"], n_rows, p=[0.4, 0.3, 0.2, 0.1]
        ),
        "value": np.random.exponential(scale=100, size=n_rows),
        "metric": np.random.normal(loc=50, scale=15, size=n_rows),
        "count": np.random.poisson(lam=10, size=n_rows),
        "binary": np.random.choice([0, 1], n_rows, p=[0.7, 0.3]),
    }

    return pd.DataFrame(data)


def basic_summary(df: pd.DataFrame, value_col: str = "value") -> Dict[str, Any]:
    """
    Generate basic summary statistics for a dataset.

    Args:
        df: pandas DataFrame
        value_col: column name to analyse

    Returns:
        Dictionary with summary statistics
    """
    if value_col not in df.columns:
        return {"error": f"Column '{value_col}' not found in DataFrame"}

    return {
        "count": len(df),
        "mean": df[value_col].mean(),
        "median": df[value_col].median(),
        "std": df[value_col].std(),
        "min": df[value_col].min(),
        "max": df[value_col].max(),
        "missing": df[value_col].isnull().sum(),
    }


def quick_histogram(df: pd.DataFrame, column: str, title: str, bins: int = 30):
    """
    Create a quick histogram using matplotlib.

    Args:
        df: pandas DataFrame
        column: column name to plot
        title: plot title
        bins: number of bins
    """
    if column not in df.columns:
        print(f"Error: Column '{column}' not found in DataFrame")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(df[column], bins=bins, alpha=0.7, edgecolor="black")
    plt.title(title or f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)
    plt.show()


def quick_scatter(df: pd.DataFrame, x_col: str, y_col: str, color_col: str, title: str):
    """
    Create a quick scatter plot using plotly.

    Args:
        df: pandas DataFrame
        x_col: x-axis column name
        y_col: y-axis column name
        color_col: optional column for color coding
        title: plot title

    Returns:
        plotly Figure object
    """
    missing_cols = [
        col for col in [x_col, y_col, color_col] if col and col not in df.columns
    ]
    if missing_cols:
        print(f"Error: Columns {missing_cols} not found in DataFrame")
        return None

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title or f"{y_col} vs {x_col}",
        labels={x_col: x_col.title(), y_col: y_col.title()},
    )

    return fig


def category_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Get value counts for a categorical column.

    Args:
        df: pandas DataFrame
        column: column name to analyse

    Returns:
        DataFrame with counts and percentages
    """
    if column not in df.columns:
        print(f"Error: Column '{column}' not found in DataFrame")
        return pd.DataFrame()

    counts = df[column].value_counts()
    percentages = (counts / len(df) * 100).round(1)

    result = pd.DataFrame(
        {
            "category": counts.index,
            "count": counts.values,
            "percentage": percentages.values,
        }
    )

    return result


def missing_values_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise missing values in the dataset.

    Args:
        df: pandas DataFrame

    Returns:
        DataFrame with missing value information
    """
    missing_info = []

    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100

        missing_info.append(
            {
                "column": col,
                "missing_count": missing_count,
                "missing_percentage": round(missing_pct, 1),
                "data_type": str(df[col].dtype),
            }
        )

    return pd.DataFrame(missing_info)


def simple_time_series(
    df: pd.DataFrame, date_col: str, value_col: str, freq: str = "M"
):
    """
    Create a simple time series aggregation and plot.

    Args:
        df: pandas DataFrame
        date_col: date column name
        value_col: value column name to aggregate
        freq: frequency for aggregation ('D', 'W', 'M', 'Y')

    Returns:
        tuple of (aggregated_data, plotly_figure)
    """
    if date_col not in df.columns or value_col not in df.columns:
        print("Error: Required columns not found in DataFrame")
        return None, None

    # Ensure date column is datetime
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    # Aggregate by time period
    if freq == "D":
        period_col = df[date_col].dt.date
    elif freq == "W":
        period_col = df[date_col].dt.to_period("W").dt.start_time
    elif freq == "M":
        period_col = df[date_col].dt.to_period("M").dt.start_time
    elif freq == "Y":
        period_col = df[date_col].dt.to_period("Y").dt.start_time
    else:
        period_col = df[date_col]

    aggregated = (
        df.groupby(period_col)[value_col].agg(["mean", "sum", "count"]).reset_index()
    )
    aggregated.columns = ["period", "mean_value", "sum_value", "count_records"]

    # Create plot
    fig = px.line(
        aggregated,
        x="period",
        y="mean_value",
        title=f"Average {value_col} Over Time",
        labels={"period": "Time Period", "mean_value": f"Average {value_col}"},
    )

    return aggregated, fig


def correlation_matrix(df: pd.DataFrame, columns):
    """
    Create a correlation matrix heatmap.

    Args:
        df: pandas DataFrame
        columns: list of columns to include (default: all numeric columns)

    Returns:
        plotly Figure object
    """
    # Select numeric columns
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = [
            col
            for col in columns
            if col in df.columns and df[col].dtype in ["int64", "float64"]
        ]

    if len(numeric_cols) < 2:
        print("Error: Need at least 2 numeric columns for correlation matrix")
        return None

    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="RdBu",
            zmid=0,
            text=corr_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False,
        )
    )

    fig.update_layout(
        title="Correlation Matrix",
        xaxis_title="Variables",
        yaxis_title="Variables",
        width=600,
        height=600,
    )

    return fig


def print_dataset_info(df: pd.DataFrame, name: str = "Dataset"):
    """
    Print basic information about a dataset.

    Args:
        df: pandas DataFrame
        name: name of the dataset
    """
    print(f"📊 {name} Information")
    print("-" * 30)
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

    # Data types
    print("\nData types:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"  {dtype}: {count} columns")

    # Missing values
    total_missing = df.isnull().sum().sum()
    missing_pct = (total_missing / (df.shape[0] * df.shape[1])) * 100
    print(f"\nMissing values: {total_missing:,} ({missing_pct:.1f}%)")

    # Date range (if any date columns)
    date_cols = df.select_dtypes(include=["datetime64"]).columns
    if len(date_cols) > 0:
        for col in date_cols:
            print(f"Date range ({col}): {df[col].min()} to {df[col].max()}")



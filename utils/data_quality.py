"""Deterministic data-quality checks for uploaded datasets."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def build_data_quality_report(df: pd.DataFrame) -> dict[str, Any]:
    """Summarize missingness, duplicate rows, constants, and IQR outliers."""
    row_count, column_count = df.shape
    cell_count = row_count * column_count
    missing_count = int(df.isna().sum().sum())
    missing_rows = int(df.isna().any(axis=1).sum()) if row_count else 0
    duplicate_rows = int(df.duplicated().sum()) if row_count else 0

    missing_by_column = [
        {
            "Column": str(column),
            "Missing": int(count),
            "Missing %": round((count / row_count) * 100, 2) if row_count else 0.0,
        }
        for column, count in df.isna().sum().items()
        if count
    ]
    missing_by_column.sort(key=lambda item: item["Missing"], reverse=True)

    constant_columns = [
        str(column)
        for column in df.columns
        if df[column].nunique(dropna=False) <= 1
    ]

    outliers: list[dict[str, Any]] = []
    for column in df.select_dtypes(include="number").columns:
        values = df[column].dropna()
        if len(values) < 4:
            continue
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        spread = q3 - q1
        if not np.isfinite(spread) or spread <= 0:
            continue
        lower = q1 - 1.5 * spread
        upper = q3 + 1.5 * spread
        count = int(((values < lower) | (values > upper)).sum())
        if count:
            outliers.append(
                {
                    "Column": str(column),
                    "Potential outliers": count,
                    "Outlier %": round((count / len(values)) * 100, 2),
                    "Lower IQR bound": float(lower),
                    "Upper IQR bound": float(upper),
                }
            )
    outliers.sort(key=lambda item: item["Potential outliers"], reverse=True)

    completeness = (
        round(((cell_count - missing_count) / cell_count) * 100, 2)
        if cell_count
        else 100.0
    )
    return {
        "rows": row_count,
        "columns": column_count,
        "cells": cell_count,
        "missing_cells": missing_count,
        "missing_rows": missing_rows,
        "duplicate_rows": duplicate_rows,
        "completeness_pct": completeness,
        "missing_by_column": missing_by_column,
        "constant_columns": constant_columns,
        "outliers": outliers,
    }

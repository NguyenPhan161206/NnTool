import pandas as pd


def get_statistics(df: pd.DataFrame) -> dict:
    stats = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include="number").columns) > 0 else {},
    }
    return stats

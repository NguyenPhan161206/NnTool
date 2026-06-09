import pandas as pd


def query_data(df: pd.DataFrame, question: str) -> str:
    q = question.lower()

    if "max" in q or "cao nhat" in q or "lon nhat" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                max_row = df.loc[df[col].idxmax()]
                return f"{col} cao nhat la {max_row[col]} (row {df[col].idxmax()})"

    if "min" in q or "thap nhat" in q or "nho nhat" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                min_row = df.loc[df[col].idxmin()]
                return f"{col} thap nhat la {min_row[col]} (row {df[col].idxmin()})"

    if "average" in q or "trung binh" in q or "mean" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                return f"{col} trung binh la {df[col].mean():.2f}"

    if "count" in q or "dem" in q or "so luong" in q:
        col = q.split()[-1]
        if col in df.columns:
            return f"{col} co {df[col].count()} gia tri (missing: {df[col].isnull().sum()})"

    return f"Da phan tich du lieu. Du lieu co {len(df)} dong, {len(df.columns)} cot."

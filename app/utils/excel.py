import pandas as pd
from typing import List, Dict, Any
from io import BytesIO

def parse_excel_to_dict(file_content: bytes) -> List[Dict[str, Any]]:
    """
    Parses an Excel file and returns a list of dictionaries.
    """
    df = pd.read_excel(BytesIO(file_content))
    # Fill NaN with None for JSON/DB compatibility
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")

def validate_columns(data: List[Dict[str, Any]], required_columns: List[str]):
    if not data:
        return False
    actual_columns = set(data[0].keys())
    return all(col in actual_columns for col in required_columns)

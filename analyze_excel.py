import pandas as pd
import sys

file_path = "c:\\Users\\karti\\OneDrive\\Desktop\\MDbackend\\data class.xlsm"

try:
    # Try reading headers and first few rows
    df = pd.read_excel(file_path, engine='openpyxl')
    print("--- ALL HEADERS ---")
    for col in df.columns:
        print(f"'{col}'")
    print("--- FIRST ROW ---")
    print(df.iloc[0].to_dict())
except Exception as e:
    print(f"Error reading file: {e}")
    # Try with openpyxl explicitly if failed
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print("--- HEADERS ---")
        print(df.columns.tolist())
        print("--- SAMPLE DATA (1 row) ---")
        print(df.head(1).to_dict(orient='records'))
    except Exception as e2:
        print(f"Error reading with openpyxl: {e2}")

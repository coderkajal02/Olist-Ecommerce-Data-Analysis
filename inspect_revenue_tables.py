
import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data" / "Raw"

file_names = [
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv"
]

for file_name in file_names:
    files = list(data_folder.rglob(file_name))

    if not files:
        print("File not found:", file_name)
        continue

    df = pd.read_csv(files[0], nrows=5)

    print("\n" + "=" * 50)
    print("FILE:", file_name)
    print("COLUMNS:", list(df.columns))
    print("\nDATA TYPES:")
    print(df.dtypes)
    print("\nSAMPLE DATA:")
    print(df.head())

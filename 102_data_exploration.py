
# ============================================================
# OLIST E-COMMERCE PROJECT
# DAY 1: ORDERS DATA LOADING, CLEANING AND ANALYSIS
# ============================================================

import pandas as pd
import csv
from pathlib import Path

# STEP 1: FIND PROJECT FOLDER

project_folder = Path.cwd()

data_folder = project_folder / "data" / "Raw"

# STEP 2: LOCATE ORIGINAL ORDERS DATASET

files = sorted(data_folder.rglob("olist_orders_dataset.csv"))

if not files:
    raise FileNotFoundError(
        "Orders dataset not found. Check data/Raw folder."
    )

orders = pd.read_csv(files[0])

print("Orders dataset loaded successfully!")

# STEP 3: UNDERSTAND THE DATASET

print("\nFirst 5 Records:")
print(orders.head())

print("\nDataset Shape:")
print(orders.shape)

print("\nColumn Names:")
print(orders.columns.tolist())

print("\nDataset Information:")
orders.info()

# STEP 4: CHECK MISSING VALUES

print("\nMissing Values:")
print(orders.isnull().sum())

# STEP 5: CHECK DUPLICATES

print("\nDuplicate Records:")
print(orders.duplicated().sum())

# STEP 6: CHECK UNIQUE VALUES

print("\nUnique Values:")
print(orders.nunique())

# STEP 7: ORDER STATUS ANALYSIS

print("\nOrder Status Count:")
print(orders["order_status"].value_counts(dropna=False))

# STEP 8: CONVERT DATE COLUMNS

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(
        orders[col],
        errors="coerce"
    )

print("\nDate Conversion Completed!")

print("\nUpdated Dataset Information:")
orders.info()

# STEP 9: CALCULATE DELIVERY DAYS

orders["delivery_days"] = (
    orders["order_delivered_customer_date"] -
    orders["order_purchase_timestamp"]
).dt.days

print("\nDelivery Days:")
print(
    orders[
        [
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "delivery_days"
        ]
    ].head()
)

# STEP 10: CREATE DELIVERY STATUS

orders["delivery_status"] = "Not Delivered"

delivered_mask = (
    orders["order_delivered_customer_date"].notna()
)

orders.loc[delivered_mask, "delivery_status"] = (
    orders.loc[
        delivered_mask,
        "order_delivered_customer_date"
    ] >
    orders.loc[
        delivered_mask,
        "order_estimated_delivery_date"
    ]
).map({
    True: "Delayed",
    False: "On Time"
})

print("\nDelivery Performance:")
print(orders["delivery_status"].value_counts())

# STEP 11: FINAL DATA QUALITY CHECK

print("\nFinal Missing Values:")
print(orders.isnull().sum())

print("\nFinal Duplicate Records:")
print(orders.duplicated().sum())

print("\nFinal Dataset Shape:")
print(orders.shape)

# STEP 12: CREATE CLEANED DATA FOLDER

cleaned_folder = project_folder / "data" / "cleaned"

cleaned_folder.mkdir(
    parents=True,
    exist_ok=True
)

# STEP 13: SAVE FINAL CLEANED CSV

output_file = cleaned_folder / "orders_cleaned.csv"

orders.to_csv(
    output_file,
    index=False,
    encoding="utf-8",
    date_format="%Y-%m-%d %H:%M:%S",
    quoting=csv.QUOTE_MINIMAL,
    quotechar='"',
    lineterminator="\n"
)

print("\nCleaned dataset saved successfully!")
print("Saved file location:", output_file.resolve())

# STEP 14: REOPEN EXPORTED CSV AND VERIFY

csv_check = pd.read_csv(
    output_file,
    encoding="utf-8",
    low_memory=False
)

print("\n========== CSV EXPORT VERIFICATION ==========")

print("\nExported Dataset Shape:")
print(csv_check.shape)

print("\nExported Order Status Counts:")
print(csv_check["order_status"].value_counts(dropna=False))

print("\nExported Total Orders:")
print(len(csv_check))

print("\nExported Column Count:")
print(len(csv_check.columns))

# STEP 15: AUTOMATIC VALIDATION

assert len(orders) == len(csv_check), (
    "ERROR: Exported row count does not match original!"
)

assert orders.shape[1] == csv_check.shape[1], (
    "ERROR: Exported column count does not match!"
)

assert orders["order_status"].value_counts(
    dropna=False
).equals(
    csv_check["order_status"].value_counts(dropna=False)
), "ERROR: Order status counts changed during export!"

print("\nSUCCESS: CSV EXPORT VERIFIED!")
print("All rows, columns and order status counts match.")

print("\n========== PROJECT SUMMARY ==========")
print("Total Orders:", len(csv_check))
print("Total Columns:", len(csv_check.columns))
print("CSV File:", output_file.name)
print("File Size (MB):", round(output_file.stat().st_size / (1024 * 1024), 2))

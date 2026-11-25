# Day 1 step 2
# loading olist orders dataset

import pandas as pd 
from pathlib import Path

# find the project folder
project_folder = Path.cwd()

# find the raw data folder
data_folder = project_folder/"data"/"Raw"

# locate the orders csv, including inside subfolders
files  = list(data_folder.rglob("olist_orders_dataset.csv"))

if not files:
    print("Orders dataset not found : check the data / raw folders.")
else: 
    orders = pd.read_csv(files[0])

    print(" Data load successfully!")

    # Display first 5 records

    print("\n first 5 records:")
    print(orders.head())
    print(orders.shape)

    # step3: understanfd dataset columns

    print("\n column Names")
    print(orders.columns)

    print("\ndataset information:")
    orders.info()

    print("\nMissing values in each columns:")
    print(orders.isnull().sum())

    print("\ntotal duplicates records:")
    print(orders.duplicated().sum())

    print("\n uniques order:")
    print(orders.nunique())
# step8 order status analysis

print("\n ordwer status copunt:")
print(orders["order_status"].value_counts())

# Date conversion

date_column = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_column:
    orders[col] = pd.to_datetime(orders[col], errors='coerce')
print(orders.info())

# calculate delivey days

orders["delivery_days"] = (
    orders["order_delivered_customer_date"] -
    orders["order_purchase_timestamp"]
).dt.days

print(orders[["order_purchase_timestamp",
              "order_delivered_customer_date",
              "delivery_days"]].head())

orders["delivery_status"] = "Not Delivered"

delivered_mask = orders["order_delivered_customer_date"].notna()

orders.loc[delivered_mask, "delivery_status"] = (
    orders.loc[delivered_mask, "order_delivered_customer_date"] >
    orders.loc[delivered_mask, "order_estimated_delivery_date"]
).map({True: "Delayed", False: "On Time"})

print(orders["delivery_status"].value_counts())

# Step 13: Check Data Quality
print("Missing Values:")
print(orders.isnull().sum())

print("\nDuplicate Records:")
print(orders.duplicated().sum())

print("\nDataset Shape:")
print(orders.shape)

#Step 14: Save Cleaned Dataset

cleaned_folder = project_folder/"data"/"cleaned"
cleaned_folder.mkdir(parents=True, exist_ok=True)

# savecleaned dataset
orders.to_csv(cleaned_folder/"orders_cleaned.csv", index=False)
print("Cleaned dataset saved successfully")

# Step 15: Basic Business Analysis
print("Total Orders:", len(orders))

print("\nOrder Status:")
print(orders["order_status"].value_counts())

print("\nAverage Delivery Days:")
print(orders["delivery_days"].mean())

print("\nDelivery Performance:")
print(orders["delivery_status"].value_counts())


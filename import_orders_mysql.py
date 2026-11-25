
print("MYSQL IMPORT SCRIPT STARTED")

import pandas as pd
import pymysql
from pathlib import Path

# STEP 1: FIND PROJECT FOLDER
project_folder = Path(__file__).resolve().parent.parent

# STEP 2: READ CLEANED CSV
csv_file = (
    project_folder / "data" / "cleaned" / "new_orders_cleaned.csv"
)

df = pd.read_csv(csv_file)

print("CSV loaded successfully!")
print("Total CSV rows:", len(df))

# STEP 3: CONNECT TO MYSQL
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="@Kajal2004",
    database="olist_analytics",
    charset="utf8mb4"
)

print("MySQL connected successfully!")

try:
    cursor = connection.cursor()

    # STEP 4: CREATE NEW TABLE
    cursor.execute("DROP TABLE IF EXISTS orders_import_python")

    cursor.execute("""
        CREATE TABLE orders_import_python (
            order_id VARCHAR(40),
            customer_id VARCHAR(40),
            order_status VARCHAR(30),
            order_purchase_timestamp DATETIME,
            order_approved_at DATETIME NULL,
            order_delivered_carrier_date DATETIME NULL,
            order_delivered_customer_date DATETIME NULL,
            order_estimated_delivery_date DATETIME,
            delivery_days DOUBLE NULL,
            delivery_status VARCHAR(30)
        )
    """)

    # STEP 5: PREPARE DATA
    df = df.astype(object).where(pd.notna(df), None)

    columns = list(df.columns)
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(f"`{col}`" for col in columns)

    insert_query = f"""
        INSERT INTO orders_import_python
        ({column_names})
        VALUES ({placeholders})
    """

    # STEP 6: IMPORT IN BATCHES
    batch_size = 500

    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start + batch_size]

        cursor.executemany(
            insert_query,
            batch.values.tolist()
        )

        connection.commit()

        print("Imported:", min(start + batch_size, len(df)))

    # STEP 7: VERIFY TOTAL
    cursor.execute("SELECT COUNT(*) FROM orders_import_python")
    print("Total records imported:", cursor.fetchone()[0])

    # STEP 8: VERIFY ORDER STATUS
    cursor.execute("""
        SELECT order_status, COUNT(*)
        FROM orders_import_python
        GROUP BY order_status
        ORDER BY COUNT(*) DESC
    """)

    print("\nOrder Status Counts:")
    for row in cursor.fetchall():
        print(row)

    print("\nIMPORT COMPLETED SUCCESSFULLY!")

except Exception as error:
    connection.rollback()
    print("IMPORT ERROR:", error)

finally:
    connection.close()
    print("MySQL connection closed.")

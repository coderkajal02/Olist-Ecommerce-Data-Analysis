
import pandas as pd
import pymysql
from pathlib import Path

print("REVENUE TABLE IMPORT STARTED")

# Locate project and CSV files
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data" / "Raw"

# Connect to MySQL
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="@Kajal2004",
    database="olist_analytics",
    charset="utf8mb4"
)

print("MySQL connected successfully!")

tables = [
    {
        "file": "olist_order_items_dataset.csv",
        "table": "order_items_import_python",
        "create": """
            CREATE TABLE order_items_import_python (
                order_id VARCHAR(40),
                order_item_id INT,
                product_id VARCHAR(40),
                seller_id VARCHAR(40),
                shipping_limit_date DATETIME,
                price DECIMAL(12,2),
                freight_value DECIMAL(12,2)
            )
        """
    },
    {
        "file": "olist_order_payments_dataset.csv",
        "table": "order_payments_import_python",
        "create": """
            CREATE TABLE order_payments_import_python (
                order_id VARCHAR(40),
                payment_sequential INT,
                payment_type VARCHAR(30),
                payment_installments INT,
                payment_value DECIMAL(12,2)
            )
        """
    }
]

try:
    cursor = connection.cursor()

    for item in tables:

        print("\nProcessing:", item["file"])

        csv_path = data_folder / item["file"]

        if not csv_path.exists():
            raise FileNotFoundError(f"File not found: {csv_path}")

        df = pd.read_csv(csv_path)

        print("CSV rows:", len(df))

        # Prepare table
        cursor.execute(f"DROP TABLE IF EXISTS `{item['table']}`")
        cursor.execute(item["create"])
        connection.commit()

        # Convert missing values to SQL NULL
        df = df.astype(object).where(pd.notna(df), None)

        columns = list(df.columns)
        column_names = ", ".join(f"`{col}`" for col in columns)
        placeholders = ", ".join(["%s"] * len(columns))

        insert_query = f"""
            INSERT INTO `{item['table']}`
            ({column_names})
            VALUES ({placeholders})
        """

        # Insert in batches
        batch_size = 500

        for start in range(0, len(df), batch_size):
            batch = df.iloc[start:start + batch_size]
            cursor.executemany(
                insert_query,
                batch.values.tolist()
            )
            connection.commit()

            print("Imported:", min(start + batch_size, len(df)))

        # Verify imported rows
        cursor.execute(
            f"SELECT COUNT(*) FROM `{item['table']}`"
        )

        imported_count = cursor.fetchone()[0]

        print("Verified rows:", imported_count)

        if imported_count != len(df):
            raise ValueError("Imported row count does not match CSV!")

    print("\nBOTH TABLES IMPORTED SUCCESSFULLY!")

except Exception as error:
    connection.rollback()
    print("IMPORT ERROR:", error)

finally:
    connection.close()
    print("MySQL connection closed.")

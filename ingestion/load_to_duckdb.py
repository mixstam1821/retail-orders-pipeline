"""
Loads raw CSVs from sample_data/ into a DuckDB warehouse file,
schema `raw`. Idempotent: drops and recreates tables each run.
"""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "sample_data"
DB_PATH = ROOT / "warehouse.duckdb"

TABLES = {
    "raw_customers": "customers.csv",
    "raw_products": "products.csv",
    "raw_orders": "orders.csv",
}


def main():
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    for table, csv_file in TABLES.items():
        csv_path = DATA_DIR / csv_file
        if not csv_path.exists():
            raise FileNotFoundError(
                f"{csv_path} not found. Run data_generator/generate_data.py first."
            )
        con.execute(f"""
            CREATE OR REPLACE TABLE raw.{table} AS
            SELECT * FROM read_csv_auto('{csv_path}', header=True);
        """)
        count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        print(f"Loaded raw.{table}: {count} rows")

    con.close()
    print(f"Warehouse ready at {DB_PATH}")


if __name__ == "__main__":
    main()

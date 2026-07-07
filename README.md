# retail-orders-pipeline

A small end-to-end ELT pipeline for e-commerce order analytics: synthetic
source data → DuckDB → dbt (staging + marts + data quality tests) →
orchestrated by Airflow.

## Architecture

```
generate_data.py          load_to_duckdb.py           dbt run / dbt test
   (Faker)          --->   (raw CSV -> DuckDB)   --->  (staging -> marts)
sample_data/*.csv          warehouse.duckdb            main_marts.*
```

- **Ingestion**: synthetic customers/products/orders CSVs, loaded as-is into
  a `raw` schema in DuckDB.
- **Transform (dbt)**:
  - `staging`: typed, renamed views on top of raw sources (`stg_customers`,
    `stg_products`, `stg_orders`)
  - `marts`: business-facing tables —
    - `mart_daily_revenue` — revenue and line-item counts per day
    - `mart_top_products` — revenue-ranked product performance
    - `mart_customer_ltv` — lifetime value, order count, first/last order per customer
- **Data quality**: 20 dbt tests — `not_null`, `unique`, `relationships`
  (referential integrity between orders/customers/products), and
  `accepted_values` on order status.
- **Orchestration**: an Airflow DAG (`retail_orders_elt_pipeline`) chains
  generate → load → dbt run → dbt test daily, so a data quality failure
  blocks the pipeline instead of silently propagating bad data downstream.

## Quickstart (no Airflow required)

```bash
pip install -r requirements.txt

make generate   # synthetic CSVs -> sample_data/
make load       # CSVs -> warehouse.duckdb (raw schema)
make run        # dbt: staging views + mart tables
make test       # 20 dbt tests, referential integrity + not-null + accepted values

# or just:
make all
```

Then explore the warehouse directly:

```bash
python3 -c "
import duckdb
con = duckdb.connect('warehouse.duckdb')
print(con.execute('select * from main_marts.mart_top_products limit 10').fetchdf())
"
```

## Running under Airflow

Copy this project to `/opt/airflow/projects/retail-orders-pipeline` (or edit
`PROJECT_DIR` in `airflow/dags/retail_pipeline_dag.py`), symlink/copy the DAG
file into your Airflow `dags/` folder, and trigger `retail_orders_elt_pipeline`
from the UI or CLI.

## Why DuckDB

No external database or credentials needed to run this locally — the whole
pipeline is reproducible with `make all`. Swapping DuckDB for Postgres/Snowflake
in production would mean changing `dbt_project/profiles.yml` and the connection
in `ingestion/load_to_duckdb.py`; the dbt models themselves are portable SQL.

## Stack

Python · Faker · DuckDB · dbt-core · dbt-duckdb · Airflow

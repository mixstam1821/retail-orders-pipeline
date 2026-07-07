"""
Orchestrates the retail orders ELT pipeline:
  1. Generate synthetic source data
  2. Load raw CSVs into DuckDB
  3. Run dbt models (staging -> marts)
  4. Run dbt tests (data quality gate)

Assumes the project lives at PROJECT_DIR (adjust if you relocate it).
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/projects/retail-orders-pipeline"
DBT_DIR = f"{PROJECT_DIR}/dbt_project"

default_args = {
    "owner": "data-eng",
    "retries": 1,
}

with DAG(
    dag_id="retail_orders_elt_pipeline",
    description="Synthetic retail data -> DuckDB -> dbt (staging + marts) -> tests",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["elt", "dbt", "duckdb", "portfolio"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command=f"python {PROJECT_DIR}/data_generator/generate_data.py",
    )

    load_raw = BashOperator(
        task_id="load_raw_to_duckdb",
        bash_command=f"python {PROJECT_DIR}/ingestion/load_to_duckdb.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test --profiles-dir .",
    )

    generate_data >> load_raw >> dbt_run >> dbt_test

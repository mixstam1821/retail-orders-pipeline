.PHONY: install generate load run test all clean

install:
	pip install -r requirements.txt

generate:
	python data_generator/generate_data.py

load:
	python ingestion/load_to_duckdb.py

run:
	cd dbt_project && dbt run --profiles-dir .

test:
	cd dbt_project && dbt test --profiles-dir .

all: generate load run test

clean:
	rm -f warehouse.duckdb
	rm -rf dbt_project/target dbt_project/logs
	rm -rf sample_data

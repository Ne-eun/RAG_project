from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Ensure the root directory is in the python path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crawling import run_crawling
from vectorization import run_vectorization

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    "crawling_vectorization_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    crawling_task = PythonOperator(
        task_id="run_crawling",
        python_callable=run_crawling,
    )

    vectorization_task = PythonOperator(
        task_id="run_vectorization",
        python_callable=run_vectorization,
    )

    crawling_task >> vectorization_task

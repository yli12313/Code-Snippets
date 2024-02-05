"""
Description: Data pipeline with Apache Airflow template.

Date: Sun. 2/4/24
"""

# Importing the required libraries.
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the extract function.
def extract(**kwargs):
    pass

# Define the process function.
def process(**kwargs):
    pass

# Defining the Directed Acyclic Graph (DAG).
dag = DAG(
    'my_data_pipeline',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily'
)

# Define the 'extract_task' operator that calls 'extract()'.
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract,
    provide_context=True,
    dag=dag
)

# Define the 'process_task' operator that calls 'process()'.
process_task = PythonOperator(
    task_id='process_task',
    python_callable=process,
    provide_context=True,
    dag=dag
)

# Set the task dependencies.
extract_task >> process_task

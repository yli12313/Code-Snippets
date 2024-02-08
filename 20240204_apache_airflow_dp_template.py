"""
Description: Data pipeline with Apache Airflow template.

Date: Sun. 2/4/24
"""

# Importing the required libraries.
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the 'extract()' function. Obviously when implementing your
# own custom pipeline, you have to change this.
def extract(**kwargs):
    pass

# Define the 'process()' function. Obviously when implementing your
# own custom pipeline, you have to change this.
def process(**kwargs):
    pass

# Defining the Directed Acyclic Graph (DAG).
dag = DAG(
    'my_data_pipeline',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily'
)

# Create PythonOperator task called 'extract_task'.
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract,
    provide_context=True,
    dag=dag
)

# Create PythonOperator task called 'process_task'.
process_task = PythonOperator(
    task_id='process_task',
    python_callable=process,
    provide_context=True,
    dag=dag
)

# Set the task dependencies.
extract_task >> process_task

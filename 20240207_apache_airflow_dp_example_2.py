"""
Description: Data pipeline with Apache Airflow example 2.

Date: Wed. 2/7/24 @ 9:22 PM EST
"""

# Importing the required libraries.
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Setting default arguments for the DAG.
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition. 
# - DAG called 'advanced_etl_pipeline'.
# - Default arguments set.
# - A description of the DAG is given.
# - 'schedule_interval': 
#     - Defines how often the DAG should be run.
#     - Can be a cron expression as a string, or a 'datetime.timedelta' object.
#     - Ex. 'timedelta(days=1)' means that the DAG will be scheduled every day.
dag = DAG(
    'advanced_etl_pipeline',
    default_args=default_args,
    description='An advanced ETL data pipeline with Apache Airflow',
    schedule_interval=timedelta(days=1),
)

# Create DummyOperator task called 'start'.
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Define the 'extract()' function. Obviously when implementing your
# own custom pipeline, you have to change this.
def extract(**kwargs):
    pass

# Define the 'transform()' function. Obviously when implementing your
# own custom pipeline, you have to change this.
def transform(**kwargs):
    pass

# Define the 'load()' function. Obviously when implementing your
# own custom pipeline, you have to change this.
def load(**kwargs):
    pass

# Create PythonOperator task called 'extract'.
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    provide_context=True,
    dag=dag,
)

# Create PythonOperator task called 'transform'.
transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

# Create PythonOperator task called 'load'.
load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    provide_context=True,
    dag=dag,
)

# Create DummyOperator task called 'end'.
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set the task dependencies.
start >> extract_task >> transform_task >> load_task >> end

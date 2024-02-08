"""
Description: Data pipeline with Apache Airflow example 3.

Date: Thu. 2/8/24 @ 4:25 PM EST
"""

# Importing the required libraries.
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

# Setting default arguments for the DAG.
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition.
dag = DAG(
    'advanced_etl_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(1)
)

# Define the Python functions:

#  - 'extract()'
#  - 'transform()'
#  - 'load()'
#  - 'data_quality_check()'

# Obviously when implementing your own custom pipeline, 
# you have to change this.

def extract(**kwargs):
    pass

def transform(**kwargs):
    pass

def load(**kwargs):
    pass

def data_quality_check(**kwargs):
    pass

# Create DummyOperator task called 'start_execution'.
start_operator = DummyOperator(
    task_id='start_execution',
    dag=dag
)

# # Create PythonOperator task called 'extract_task'.
extract_operator = PythonOperator(
    task_id='extract_task',
    python_callable=extract,
    provide_context=True,
    dag=dag
)

# Create PythonOperator task called 'transform_task'.
transform_operator = PythonOperator(
    task_id='transform_task',
    python_callable=transform,
    provide_context=True,
    dag=dag
)

# Create PythonOperator task called 'load_task'.
load_operator = PythonOperator(
    task_id='load_task',
    python_callable=load,
    provide_context=True,
    dag=dag
)

# Create PythonOperator task called 'data_quality_check_task'.
data_quality_check_operator = PythonOperator(
    task_id='data_quality_check_task',
    python_callable=data_quality_check,
    provide_context=True,
    dag=dag
)

# Create EmailOperator task called 'send_email'.
email_operator = EmailOperator(
    task_id='send_email',
    to='your-email@example.com',
    subject='Airflow Alert',
    html_content="""<h3>Email sent from Airflow</h3>
                   <b>Airflow alert: </b> Please check your Airflow pipeline.""",
    dag=dag
)

# Create DummyOperator task called 'end_execution'.
end_operator = DummyOperator(
    task_id='end_execution',
    dag=dag
)

# Set the task dependencies.
start_operator >> extract_operator
extract_operator >> transform_operator
transform_operator >> load_operator
load_operator >> data_quality_check_operator
data_quality_check_operator >> email_operator
email_operator >> end_operator

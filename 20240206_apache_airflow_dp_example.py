"""
Description: Data pipeline with Apache Airflow example.

Date: Tue. 2/6/24 @ 2:01 PM EST
"""

# Importing the required libraries.
import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.postgres_hook import PostgresHook
import requests
import json

# Defining a Python function called 'extract()'.
def extract(**kwargs):
    url = 'https://api.example.com/data'
    response = requests.get(url)
    data = response.json()

    # Using Airflow's XCom (cross-communication) feature
    # to pass the extracted data to other tasks.
    # - 'ti': Shorthand for "task instance".
    # - xcom_push(): Push data into XCom.
    # - 'data': Key under which the data will be stored.
    # - data: Actual data itself.
    kwargs['ti'].xcom_push(key='data', value=data)

# Defining a Python function called 'transform()'.
def transform(**kwargs):
    # Retrieves the task instance ('ti') from the 'kwargs' dictionary.
    ti = kwargs['ti']
    # Retrieves data stored in XCom under key 'data'.
    data = ti.xcom_pull(key='data')
    transformed_data = [item['value'] for item in data]
    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)

# Defining a Python function called 'load()'.
def load(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(key='transformed_data')
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    for item in transformed_data:
        pg_hook.run(f"INSERT INTO table_name VALUES ({item});")

# Setting default arguments for the DAG.
default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2023, 6, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

# DAG definition. DAG called 'data_pipeline' with default
# arguments set to run daily. All the tasks have to fall within
# the scope of this 'dag'. Moreover, the code line that sets
# the task dependencies have to fall within this scope!
with DAG('data_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         ) as dag:

    # Create DummyOperator task called 'start'.
    start = DummyOperator(task_id='start')

    # 1) Create PythonOperator task called 'extract'.
    # 2) The 'extract()' function should be called when this
    # task is executed.
    # 3) The execution context (i.e. execution date, the task 
    # instance, etc.) will be passed to the 'extract()' function.
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract,
        provide_context=True,
    )

    # Create PythonOperator task called 'transform'.
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform,
        provide_context=True,
    )

    # Create PythonOperator task called 'load'.
    load = PythonOperator(
        task_id='load',
        python_callable=load,
        provide_context=True,
    )

    # Create DummyOperator task called 'end'.
    end = DummyOperator(task_id='end')

    # Set the task dependencies.
    start >> extract >> transform >> load >> end

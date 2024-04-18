"""
Description: Apache Airflow dynamic task mapping example.

Date: Thu. 4/18/24 @ 10:50 PM EST

Description:
Dynamic Task Mapping is a powerful feature in Apache Airflow that allows a workflow to create
a number of tasks at runtime based on current data.
  - Instead of the DAG author having to know in advance how many tasks would be needed, the 
  scheduler can create tasks based on the output of a previous task.
  - This is similar to defining your tasks in a for loop, but instead of having the DAG file fetch
  the data and do that itself, the scheduler does this.
  - Right before a mapped task is executed, the scheduler will create n copies of the task, one for 
  each input.
  - It is also possible to have a task operate on the collected output of a mapped task, commonly
  known as map and reduce.

In the example below, add_one is a mapped task that operates on each element in the list [1, 2, 3].
The sum_it task then operates on the collected output of add_one.

Dynamic Task Mapping is a paradigm shift for DAG design in Airflow, as it allows you to create 
tasks based on the current runtime environment without having to change your DAG code.
"""

from __future__ import annotations
from datetime import datetime
from airflow.decorators import task
from airflow.models.dag import DAG

with DAG(dag_id="example_dynamic_task_mapping", start_date=datetime(2022, 3, 4)) as dag:
  @task
  def add_one(x: int):
    return x + 1

  @task
  def sum_it(values):
    total = sum(values)
    print(f"Total was {total}")

  added_values = add_one.expand(x=[1, 2, 3])
  sum_it(added_values)


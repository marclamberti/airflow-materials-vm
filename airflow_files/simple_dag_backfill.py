import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner': 'airflow',
	'start_date': dt.datetime(2020, 1, 1),
	'concurrency': 1,
	'retries': 0
}

with DAG('simple_dag_backfill',
	default_args=default_args,
	schedule_interval='@daily') as dag:
	task_hello = BashOperator(task_id='hello', bash_command='echo "hello!"')
	task_bye = BashOperator(task_id='bye', bash_command='echo "bye!"')
	task_hello >> task_bye

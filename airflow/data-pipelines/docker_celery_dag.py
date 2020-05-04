import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
	'owner': 'airflow',
	'start_date': dt.datetime(2020, 1, 1, 11, 30, 00),
	'retries': 0
}

with DAG('docker_celery_dag',
	default_args=default_args,
	schedule_interval='*/5 * * * *',
	catchup=False) as dag:

	opr_create_schema = PostgresOperator(task_id="create_schema_task", sql="CREATE SCHEMA IF NOT EXISTS docker_celery;", autocommit=True, database='airflow')
	opr_create_table = PostgresOperator(task_id="create_table_task", sql="CREATE TABLE IF NOT EXISTS docker_celery.task(id VARCHAR(50) PRIMARY KEY, timestamp TIMESTAMP);", autocommit=True, database='airflow')	

	opr_end = BashOperator(task_id='opr_end', bash_command='echo "Done"')

	opr_create_schema >> opr_create_table

	# Dynamic Definition of your DAG!!
	for counter in range(1, 4):
		task_id='opr_insert_' + str(counter)
		task_date=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		opr_insert = PostgresOperator(task_id=task_id, 
						sql="INSERT INTO docker_celery.task (id, timestamp) VALUES ('" + task_id + "_" + task_date  + "', '" + task_date + "');",
						autocommit=True,
						database='airflow')
		opr_create_table >> opr_insert >> opr_end




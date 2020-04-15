from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner': 'airflow',
	'depend_on_past': False,
	'start_date': datetime(2020, 1, 1),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

def get_activated_sources():
	request = "SELECT * FROM course.source"
	pg_hook = PostgresHook(postgres_conn_id="postgre_sql", schema="airflow_mdb") # This connection must be set from the Connection view in Airflow UI
	connection = pg_hook.get_conn() # Gets the connection from PostgreHook
	cursor = connection.cursor() # Gets a cursor to the postgreSQL database. Look at https://www.postgresql.org/docs/9.2/plpgsql-cursors.html for more information
	cursor.execute(request) # Executes the request
	sources = cursor.fetchall() # Fetchs all the data from the executed request
	for source in sources: # Does a simple print of each source to show that the hook works well. More on the next lesson
		print("Source: {0} - activated: {1}".format(source[0], source[1]))
	return sources

with DAG('hook_dag',
	default_args=default_args,
	schedule_interval='@once',
	catchup=False) as dag:

	start_task = DummyOperator(task_id='start_task')
	hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_sources)
	start_task >> hook_task
		

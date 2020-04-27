from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
	'owner': 'airflow',
	'depend_on_past': False,
	'start_date': datetime(2020, 1, 1),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

# Read the table sources to fetch the data and return the name of first source having its column "activated" sets to true
# No need to call xcom_push here since we use the keyword "return" which has the same effect.
def get_activated_sources():
	request = "SELECT * FROM sources"
	mysql_hook = MySqlHook(mysql_conn_id="mysql", schema="airflow_mdb")
	connection = mysql_hook.get_conn()
	cursor = connection.cursor()
	cursor.execute(request)
	sources = cursor.fetchall()
	for source in sources:
		if source[1]:
			return source[0]
	return None

def source_to_use(**kwargs):
	ti = kwargs['ti']
	source = ti.xcom_pull(task_ids='hook_task')
	print("source fetch from XCOM: {}".format(source))

with DAG('xcom_dag',
	default_args=default_args,
	schedule_interval='@once',
	catchup=False) as dag:

	start_task = DummyOperator(task_id='start_task')
	hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_sources)
	xcom_task = PythonOperator(task_id='xcom_task', python_callable=source_to_use, provide_context=True)
	start_task >> hook_task >> xcom_task
		

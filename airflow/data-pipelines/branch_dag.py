from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
	'owner': 'airflow',
	'depend_on_past': False,
	'start_date': datetime(2020, 1, 1),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

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
	return source

def check_for_activated_source(**kwargs):
	ti = kwargs['ti']
	return ti.xcom_pull(task_ids='xcom_task').lower()

with DAG('branch_dag',
	default_args=default_args,
	schedule_interval='@once') as dag:

	start_task 	    = DummyOperator(task_id='start_task')
	hook_task 	    = PythonOperator(task_id='hook_task', python_callable=get_activated_sources)
	xcom_task 	    = PythonOperator(task_id='xcom_task', python_callable=source_to_use, provide_context=True)
	branch_task 	= BranchPythonOperator(task_id='branch_task', python_callable=check_for_activated_source, provide_context=True)
	mysql_task 	    = BashOperator(task_id='mysql', bash_command='echo "MYSQL is activated"')
	postgresql_task = BashOperator(task_id='postgresql', bash_command='echo "PostgreSQL is activated"')
	s3_task 	    = BashOperator(task_id='s3', bash_command='echo "S3 is activated"')
	mongo_task 	    = BashOperator(task_id='mongo', bash_command='echo "Mongo is activated"')
	
	start_task >> hook_task >> xcom_task >> branch_task
	branch_task >> mysql_task
	branch_task >> postgresql_task
	branch_task >> s3_task
	branch_task >> mongo_task
	

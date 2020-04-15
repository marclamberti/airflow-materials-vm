import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.elasticsearch_plugin import ElasticsearchHook

default_args = {
        'owner': 'airflow',
        'start_date': dt.datetime(2020, 1, 1),
        'concurrency': 1,
        'retries': 0
}

def do_some_stuff():
	es_hook = ElasticsearchHook()
	print(es_hook.info())

with DAG('plugin_hook_dag',
        default_args=default_args,
        schedule_interval='@once',
	catchup=False
	) as dag:

	hook_es = PythonOperator(task_id='hook_es', python_callable=do_some_stuff)
	opr_end = BashOperator(task_id='opr_end', bash_command='echo "Done"')
	hook_es >> opr_end

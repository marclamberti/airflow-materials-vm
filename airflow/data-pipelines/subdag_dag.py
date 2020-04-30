from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.dummy_operator import DummyOperator
from subdag_factory import subdag_factory

PARENT_DAG_NAME='subdag_dag'
SUBDAG_DAG_NAME='subdag'

with DAG(
	dag_id=PARENT_DAG_NAME,
	schedule_interval='@daily',
	start_date=datetime(2020, 1, 1, 10, 00, 00),
	catchup=False
) as dag:
	start_task = DummyOperator(task_id='start')	
	subdag_task = SubDagOperator(
			subdag=subdag_factory(PARENT_DAG_NAME, SUBDAG_DAG_NAME, dag.start_date, dag.schedule_interval),
			task_id=SUBDAG_DAG_NAME
		)
	end_task = DummyOperator(task_id='end')
	start_task >> subdag_task >> end_task

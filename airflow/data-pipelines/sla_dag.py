from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, datetime

def log_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    print("SLA was missed on DAG {0}s by task id {1}s with task list: {2} which are " \
	"blocking task id {3}s with task list: {4}".format(dag.dag_id, slas, task_list, blocking_tis, blocking_task_list))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1, 23, 15, 0),
    'email': None,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG('sla_dag', default_args=default_args, sla_miss_callback=log_sla_miss, schedule_interval="*/1 * * * *", catchup=False) as dag:

	t0 = DummyOperator(task_id='t0')

	t1 = BashOperator(task_id='t1', bash_command='sleep 15', sla=timedelta(seconds=5), retries=0)

	t0 >> t1

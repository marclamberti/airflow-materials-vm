# load the dependencies
from airflow import DAG
from datetime import date, timedelta, datetime

# default_args are the default arguments applied to all inherited tasks
DAG_DEFAULT_ARGS = {
	'owner': 'airflow',
	'depends_on_past': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

with DAG('twitter_dag_v1', start_date=datetime(2018, 10, 1), schedule_interval="@daily", default_args=DAG_DEFAULT_ARGS, catchup=False) as dag:
	None

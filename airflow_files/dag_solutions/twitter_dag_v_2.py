# load the dependencies
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta, datetime

import fetching_tweet
import cleaning_tweet

# default_args are the default arguments applied to the Dag's tasks
DAG_DEFAULT_ARGS = {
	'owner': 'airflow',
	'depends_on_past': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

with DAG('twitter_dag_v2', start_date=datetime(2018, 10, 1), schedule_interval="@daily", default_args=DAG_DEFAULT_ARGS, catchup=False) as dag:
	waiting_file_task = FileSensor(task_id="waiting_file_task", fs_conn_id="fs_default", filepath="/home/airflow/airflow_files/data.csv", poke_interval=5)

	fetching_tweet_task = PythonOperator(task_id="fetching_tweet_task", python_callable=fetching_tweet.main)

	cleaning_tweet_task = PythonOperator(task_id="cleaning_tweet_task", python_callable=cleaning_tweet.main)

	load_into_hdfs_task = BashOperator(task_id="load_into_hdfs_task", bash_command="hadoop fs -put -f /tmp/data_cleaned.csv /tmp/")

	transfer_into_hive_task = HiveOperator(task_id="transfer_into_hive_task", hql="LOAD DATA INPATH '/tmp/data_cleaned.csv' INTO TABLE tweets PARTITION(dt='2018-10-01')")

	waiting_file_task >> fetching_tweet_task >> cleaning_tweet_task >> load_into_hdfs_task >> transfer_into_hive_task

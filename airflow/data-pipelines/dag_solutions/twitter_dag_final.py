# load the dependencie

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta
from datetime import datetime as dt

# import the script files which are going be execute as Tasks by the DAG

import fetching_tweet
import cleaning_tweet

# Local directory where the data file ise
LOCAL_DIR='/tmp/'

# HDFS directory where the data file will be uploaded
HDFS_DIR='/tmp/'

# each DAG must have a unique identifier
DAG_ID = 'twitter_dag_final'

# start_time is a datetime object to indicate
# at which time your DAG should start (can be either in the past or future)
DAG_START_DATE=airflow.utils.dates.days_ago(1)

# schedule interval is a timedelta object
# here our DAG will be run every day
DAG_SCHEDULE_INTERVAL="@daily"

# default_args are the default arguments applied to the DAG
# and all inherited tasks
DAG_DEFAULT_ARGS = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': DAG_START_DATE,
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

yesterday = date.today() - timedelta(days=1)
dt = yesterday.strftime("%Y-%m-%d")

with DAG(
	DAG_ID,
	default_args=DAG_DEFAULT_ARGS,
	schedule_interval=DAG_SCHEDULE_INTERVAL
	) as dag:
	
	# Initialise a FileSensor to watch if a new file is coming.
	# task_id must be unique
	# poke_interval give the time in seconds that the job should wait between each tries
	waiting_file_task = FileSensor(task_id='waiting_file_task', fs_conn_id='fs_default', filepath='/home/airflow/airflow_files/data.csv', poke_interval=15, dag=dag)

	# Initialise a PythonOperator to execute the fetching_tweet.py script
	fetching_tweet_task = PythonOperator(task_id='fetching_tweet_task', python_callable=fetching_tweet.main, dag=dag)

	# Initialise another PythonOperator to execute the cleaning_tweet.py script
	cleaning_tweet_task = PythonOperator(task_id='cleaning_tweet_task', python_callable=cleaning_tweet.main, dag=dag)

	# Initialise a BashOperator to upload the file into HDFS
	filename='data_cleaned.csv'
	load_into_hdfs_task = BashOperator(task_id='load_into_hdfs_task', bash_command='hadoop fs -put -f ' + LOCAL_DIR + filename + ' ' + HDFS_DIR, dag=dag)
	
	# Initialise a HiveOperator to transfer data from HDFS to HIVE table
	load_into_hive_task = HiveOperator(task_id='transfer_into_hive_task', hql="LOAD DATA INPATH '" + HDFS_DIR + filename + "' INTO TABLE tweets PARTITION(dt='" + dt + "')", dag=dag)

	waiting_file_task >> fetching_tweet_task >> cleaning_tweet_task >> load_into_hdfs_task >> load_into_hive_task

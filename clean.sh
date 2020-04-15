mv /home/airflow/airflow/dags/data /home/airflow/airflow_files
rm -rf /tmp/data_fetched.csv
rm -rf /tmp/data_cleaned.csv
hadoop fs -rm /tmp/data_cleaned.csv
hive -e "TRUNCATE TABLE tweets;" 

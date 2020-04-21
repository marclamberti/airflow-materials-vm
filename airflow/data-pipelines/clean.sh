#!/bin/bash

rm -rf /home/vagrant/airflow/dags/data
rm -rf /tmp/data_cleaned.csv
rm -rf /tmp/data_fetched.csv
hive -e "DROP TABLE tweets;"
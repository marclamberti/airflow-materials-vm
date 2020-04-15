#!/bin/bash

/opt/hadoop/sbin/start-dfs.sh
sudo -E -u airflow bash -c '/opt/hive/bin/hive --service metastore &'
/opt/spark/sbin/start-master.sh
/opt/spark/sbin/start-slaves.sh

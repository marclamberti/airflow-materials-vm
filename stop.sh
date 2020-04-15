#!/bin/bash

/opt/hadoop/sbin/stop-dfs.sh
sudo -E -u airflow bash -c 'kill `pgrep -f hive`'
/opt/spark/sbin/stop-master.sh
/opt/spark/sbin/stop-slaves.sh

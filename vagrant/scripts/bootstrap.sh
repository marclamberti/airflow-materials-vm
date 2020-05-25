#!/bin/bash

# If you restart your VM then the Hadoop/Spark/Hive services will be started by this script.
# Due to the config "node.vm.provision :shell, path: "scripts/bootstrap.sh", run: 'always'" on Vagrantfile

source "/home/vagrant/vagrant-scripts/common.sh"

systemctl start mysql.service
systemctl start rabbitmq-server
systemctl start elasticsearch
systemctl start kibana
/home/vagrant/vagrant-scripts/start-hadoop.sh	# Starts the namenode/datanode plus yarn.
/home/vagrant/vagrant-scripts/start-hive.sh		# Start hiveserver2 plus metastore service.
/home/vagrant/vagrant-scripts/start-spark.sh	# Start Spark history server.

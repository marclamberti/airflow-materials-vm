#!/bin/bash

#
# Version information is defined the versions.sh file
#
source "/vagrant/scripts/versions.sh"

# Curl options
CURL_OPTS="-Ss --retry 10 "

# java
JAVA_ARCHIVE=jdk-8u51-linux-x64.gz
JAVA_MYSQL_CONNECTOR_VERSION=5.1.40
JAVA_MYSQL_CONNECTOR_JAR=mysql-connector-java-${JAVA_MYSQL_CONNECTOR_VERSION}.jar
# 
JAVA_MYSQL_CONNECTOR_DOWNLOAD=https://repo.maven.apache.org/maven2/mysql/mysql-connector-java/${JAVA_MYSQL_CONNECTOR_VERSION}/mysql-connector-java-${JAVA_MYSQL_CONNECTOR_VERSION}.jar

# hadoop
HADOOP_PREFIX=/usr/local/hadoop
HADOOP_CONF=$HADOOP_PREFIX/etc/hadoop
HADOOP_ARCHIVE=$HADOOP_VERSION.tar.gz
HADOOP_MIRROR_DOWNLOAD=http://archive.apache.org/dist/hadoop/core/$HADOOP_VERSION/$HADOOP_ARCHIVE
HADOOP_RES_DIR=/vagrant/resources/hadoop

# Yarn
HADOOP_YARN_HOME=$HADOOP_PREFIX

# hive
HIVE_ARCHIVE=apache-hive-${HIVE_VERSION}-bin.tar.gz
HIVE_MIRROR_DOWNLOAD=http://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/$HIVE_ARCHIVE
HIVE_RES_DIR=/vagrant/resources/hive
HIVE_CONF=/usr/local/hive/conf
HIVE_PREFIX=/usr/local/hive
HIVE_EXEC_JAR=${HIVE_PREFIX}/lib/hive-exec-${HIVE_VERSION}.jar

# spark
SPARK_ARCHIVE=$SPARK_VERSION-bin-hadoop2.tgz
SPARK_MIRROR_DOWNLOAD=http://archive.apache.org/dist/spark/$SPARK_VERSION/$SPARK_VERSION-bin-hadoop2.7.tgz
SPARK_RES_DIR=/vagrant/resources/spark
SPARK_HOME=/usr/local/spark
SPARK_CONF=${SPARK_HOME}/conf
SPARK_CONF_DIR=${SPARK_CONF}

# elasticsearch
ES_ARCHIVE=elasticsearch-$ES_VERSION-amd64.deb
ES_MIRROR_DOWNLOAD=https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-$ES_VERSION-amd64.deb
ES_RES_DIR=/vagrant/resources/es
ES_CONF=elasticsearch.yml
ES_CONF_DIR=/etc/elasticsearch/

# kibana
KIBANA_ARCHIVE=kibana-$KIBANA_VERSION-amd64.deb
KIBANA_MIRROR_DOWNLOAD=https://artifacts.elastic.co/downloads/kibana/kibana-$KIBANA_VERSION-amd64.deb
KIBANA_RES_DIR=/vagrant/resources/kibana
KIBANA_CONF=kibana.yml
KIBANA_CONF_DIR=/etc/kibana/

# rabbitmq
ERLANG_ARCHIVE=esl-erlang_$ERLANG_VERSION~ubuntu~xenial_amd64.deb
ERLANG_MIRROR_DOWNLOAD=https://packages.erlang-solutions.com/erlang/debian/pool/esl-erlang_$ERLANG_VERSION~ubuntu~xenial_amd64.deb

# virtualenv
VENV_RES_DIR=/vagrant/resources/virtualenv

# ssh
SSH_RES_DIR=/vagrant/resources/ssh
RES_SSH_COPYID_ORIGINAL=$SSH_RES_DIR/ssh-copy-id.original
RES_SSH_COPYID_MODIFIED=$SSH_RES_DIR/ssh-copy-id.modified
RES_SSH_CONFIG=$SSH_RES_DIR/config

# vim
VIM_RES_DIR=/vagrant/resources/vim

# passwords for mysql
MYSQL_CONF=mysqld.cnf
MYSQL_ROOT_PASSWORD=root
MYSQL_AIRFLOW_PASSWORD=airflow
MYSQL_CONF_DIR=/etc/mysql/mysql.conf.d/

# Zeppelin 
ZEPPELIN_RELEASE=zeppelin-${ZEPPELIN_VERSION}-bin-netinst
ZEPPELIN_ARCHIVE=${ZEPPELIN_RELEASE}.tgz
ZEPPELIN_MIRROR_DOWNLOAD=http://www-eu.apache.org/dist/zeppelin/zeppelin-${ZEPPELIN_VERSION}/${ZEPPELIN_ARCHIVE}
ZEPPELIN_RES_DIR=/vagrant/resources/zeppelin
ZEPPELIN_TARGET=/home/ubuntu


# Utility functions
function resourceExists {
	FILE=/vagrant/resources/$1
	if [ -e $FILE ]
	then
		return 0
	else
		return 1
	fi
}

function fileExists {
	FILE=$1
	if [ -e $FILE ]
	then
		return 0
	else
		return 1
	fi
}

#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh"

function installVenv {
    apt-get -y install build-essential checkinstall
    apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    apt-get install libmysqlclient-dev
    cd /usr/src
    wget https://www.python.org/ftp/python/3.5.6/Python-3.5.6.tgz
    tar xzf Python-3.5.6.tgz
    cd Python-3.5.6
    ./configure --enable-optimizations
    make altinstall
    cd /home/vagrant
    pip install --upgrade pip
    python3.5 -m venv .sandbox
    chmod +x .sandbox/bin/activate
    chown -R vagrant: . 
}

echo "setup python virtual environment"

installVenv

echo "python virtual environment setup complete"

#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh"

function installVenv {
    apt-get install python3-setuptools
    easy_install3 pip
    pip install virtualenv
    virtualenv .sandbox
    chmod +x .sandbox/bin/activate
}

echo "setup python virtual environment"

installVenv

echo "python virtual environment setup complete"

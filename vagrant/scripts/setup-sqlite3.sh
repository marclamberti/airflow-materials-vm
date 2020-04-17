#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh"

function setupMaterials {
    echo "setup sqlite3"
    apt-get -y update
    apt-get install sqlite3
}

echo "setup sqlite3"

setupSqlite

echo "sqlite3 setup complete"

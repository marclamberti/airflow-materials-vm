#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh"

function setupMaterials {
    echo "setup materials"
    cp -f /vagrant/resources/materials/update_materials.sh /home/vagrant
    chmod +x /home/vagrant/update_materials.sh
    /home/vagrant/update_materials.sh
}

echo "setup materials"

setupMaterials

echo "materials setup complete"

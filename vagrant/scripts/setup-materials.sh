#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh" || source "/home/vagrant/vagrant-scripts/common.sh"

function setupMaterials {
    echo "setup materials"
    cp -f /vagrant/resources/materials/update_materials.sh /home/vagrant
    chmod +x /home/vagrant/update_materials.sh
    /home/vagrant/update_materials.sh
    chmod +x /home/vagrant/airflow-materials/data-pipelines/clean.sh
}

function setupBootstrap {
    sudo -E cp /home/vagrant/vagrant-scripts/bootstrap.sh /etc/init.d/
    sudo -E chmod +x /etc/init.d/bootstrap.sh
    sudo -E update-rc.d bootstrap.sh defaults
    sudo -E /etc/init.d/bootstrap.sh
}

echo "setup materials"

setupMaterials
setupBootstrap

echo "materials setup complete"

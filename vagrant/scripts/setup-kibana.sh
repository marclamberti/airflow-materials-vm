#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh" || source "/home/vagrant/vagrant-scripts/common.sh"

function installLocalKibana {
	echo "install kibana from local file"
	FILE=/vagrant/resources/$KIBANA_ARCHIVE
    dpkg -i $FILE
}

function installRemoteKibana {
	echo "install kibana from remote file"
	curl ${CURL_OPTS} -o /vagrant/resources/$KIBANA_ARCHIVE -O -L $KIBANA_MIRROR_DOWNLOAD
	dpkg -i /vagrant/resources/$KIBANA_ARCHIVE
}

function setupKibana {
    echo "setup kibana"
    cp -f /vagrant/resources/kibana/$KIBANA_CONF ${KIBANA_CONF_DIR}
}

function installKibana {
	if resourceExists $KIBANA_ARCHIVE; then
		installLocalKibana
	else
		installRemoteKibana
	fi
}

function setupEnvVars {
	echo "creating kibana environment variables"
	cp -f $KIBANA_RES_DIR/kibana.sh /etc/profile.d/kibana.sh
	. /etc/profile.d/kibana.sh
}

function startServices {
	echo "starting Kibana service"
	service kibana start
}

echo "setup kibana"

installKibana
setupKibana
setupEnvVars
startServices

echo "kibana setup complete"

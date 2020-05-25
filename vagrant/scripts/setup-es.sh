#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh" || source "/home/vagrant/vagrant-scripts/common.sh"

function installLocalES {
	echo "install elasticsearch from local file"
	FILE=/vagrant/resources/$ES_ARCHIVE
    dpkg -i $FILE
}

function installRemoteES {
	echo "install elasticsearch from remote file"
	curl ${CURL_OPTS} -o /vagrant/resources/$ES_ARCHIVE -O -L $ES_MIRROR_DOWNLOAD
	dpkg -i /vagrant/resources/$ES_ARCHIVE
}

function setupES {
    echo "setup elasticsearch"
    cp -f /vagrant/resources/es/$ES_CONF ${ES_CONF_DIR}
}

function installES {
	if resourceExists $ES_ARCHIVE; then
		installLocalES
	else
		installRemoteES
	fi
}

function setupEnvVars {
	echo "creating es environment variables"
	cp -f $ES_RES_DIR/es.sh /etc/profile.d/es.sh
	. /etc/profile.d/es.sh
}

function startServices {
	echo "starting ES service"
	service elasticsearch start
}

echo "setup elasticsearch"

installES
setupES
setupEnvVars
startServices

echo "elasticsearch setup complete"

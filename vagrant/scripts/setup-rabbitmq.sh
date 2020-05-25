#!/bin/bash

# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-2-x/topics/cdh_ig_spark_configure.html

source "/vagrant/scripts/common.sh" || source "/home/vagrant/vagrant-scripts/common.sh"

function installLocalRabbitmq {
	echo "install rabbitmq from local file"
	FILE=/vagrant/resources/$ERLANG_ARCHIVE
    dpkg -i $FILE
}

function installRemoteRabbitmq {
	echo "install rabbitmq from remote file"
	curl ${CURL_OPTS} -o /vagrant/resources/$ERLANG_ARCHIVE -O -L $ERLANG_MIRROR_DOWNLOAD
	dpkg -i /vagrant/resources/$ERLANG_ARCHIVE
}

function setupRabbitmq {
    echo "setup rabbitmq"
    #cp -f /vagrant/resources/rabbitmq/$RABBITMQ_CONF ${RABBITMQ_CONF_DIR}
}

function installRabbitmq {
	if resourceExists $ERLANG_ARCHIVE; then
		installLocalRabbitmq
	else
    	installRemoteRabbitmq
	fi
    apt-get -y update
    apt-get -y upgrade
    apt-get -y -f install
	if resourceExists $ERLANG_ARCHIVE; then
		installLocalRabbitmq
	else
    	installRemoteRabbitmq
	fi
    echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
    wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
    apt-get -y update
    apt-get -y install rabbitmq-server
}

function setupEnvVars {
	echo "creating rabbitmq environment variables"
	#cp -f $RABBITMQ_RES_DIR/rabbitmq.sh /etc/profile.d/rabbitmq.sh
	#. /etc/profile.d/rabbitmq.sh
}

function startServices {
	echo "starting rabbitmq service"
    service rabbitmq-server start
}

function initUser {
    rabbitmqctl add_user rabbitmq rabbitmq
    rabbitmqctl set_user_tags rabbitmq administrator
    rabbitmqctl set_permissions -p / rabbitmq ".*" ".*" ".*"
}

function initConsole {
    rabbitmq-plugins enable rabbitmq_management
    chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/
}

echo "setup rabbitmq"

installRabbitmq
setupRabbitmq
setupEnvVars
startServices
initUser
initConsole

echo "rabbitmq setup complete"

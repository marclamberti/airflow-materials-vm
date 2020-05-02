#!/bin/bash

source "/vagrant/scripts/common.sh"

function installDocker {
	apt-get install curl
    curl --fail --silent --show-error --location https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    apt-get install software-properties-common
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-get install -y docker-ce
    usermod -aG docker vagrant
}

function installDockerCompose {
    curl -L https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
}

echo "setup docker and docker-compose"

installDocker
installDockerCompose

echo "setup docker and docker-compose done"

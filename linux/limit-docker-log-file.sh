#!/bin/bash

mkdir /etc/docker
touch /etc/docker/daemon.json
echo -e "{\"log-opts\":{\"max-size\":\"20m\",\"max-file\":\"3\"}}" > /etc/docker/daemon.json

apt-get install -y docker.io
service docker restart

#!/bin/bash


mkdir /etc/docker
touch /etc/docker/daemon.json

# todo: enhance dict
echo -e "{\n" > /etc/docker/daemon.json
# user namespace remap
echo -e "\"userns-remap\": \"default\"\n" > /etc/docker/daemon.json
# log file size and number
echo -e "\"log-opts\":{\"max-size\":\"20m\",\"max-file\":\"3\"}\n" > /etc/docker/daemon.json
echo -e "}" > /etc/docker/daemon.json

apt-get install -y docker.io
service docker restart

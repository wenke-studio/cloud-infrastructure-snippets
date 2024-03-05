#!/bin/bash

systemctl list-timers

sed -i 's/APT::Periodic::Update-Package-Lists "1"/APT::Periodic::Update-Package-Lists "0"/' /etc/apt/apt.conf.d/20auto-upgrades

apt-get remove -y unattended-upgrades

systemctl stop apt-daily.timer
systemctl disable apt-daily.timer

systemctl stop apt-daily.service
systemctl disable apt-daily.service

systemctl stop apt-daily-upgrade.timer
systemctl disable apt-daily-upgrade.timer

systemctl stop apt-daily-upgrade.service
systemctl disable apt-daily-upgrade.service

systemctl kill --kill-who=all apt-daily.service
systemctl daemon-reload

systemctl list-timers

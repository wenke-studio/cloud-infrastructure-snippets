#!/bin/bash

echo -e "* soft nofile 65535\n* hard nofile 65535" >> /etc/security/limits.conf

#journalctl --vacuum-time=1w
#journalctl --vacuum-size=50M

echo -e "SystemMaxUse=100M" >> /etc/systemd/journald.conf
echo -e "SystemMaxFileSize=20M" >> /etc/systemd/journald.conf

systemctl restart systemd-journald.service

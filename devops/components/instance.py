"""Provides a instance component to create resources for instance"""

from __future__ import annotations

from pathlib import Path

import pulumi
from integrator.aws import ec2, iam
from integrator.aws.ec2.ami import Ubuntu

BASE_DIR = Path(__file__).resolve().parent.parent


class InstanceComponent:
    """Create a instance with launch template, role, security group, and subnet."""

    def __init__(
        self, name: str, vpc: ec2.Vpc, cidr_block: str, key_pair: ec2.KeyPair
    ) -> None:
        role = iam.InstanceRole(name)

        statements = []  # todo: TBD
        if statements:
            role.create_policy(name, statements=statements)

        subnet = vpc.create_public_subnet(
            name, availability_zone=vpc.availability_zones[0], cidr_block=cidr_block
        )

        security_group = vpc.create_security_group(name)

        ubuntu = Ubuntu()

        user_data = ec2.UserData(BASE_DIR / "user_data" / "instance.sh")
        user_data.execute(BASE_DIR / "user_data" / f"{name}.sh")

        launch_template = ec2.LaunchTemplate(
            name,
            role=role,
            image=ubuntu.jammy_22,
            user_data=user_data,
            key_pair=key_pair,
            block_device_mappings=[
                {
                    "device_name": "/dev/sda1",
                    "ebs": {
                        "delete_on_termination": True,
                        "volume_size": 50,
                        "volume_type": "gp3",
                    },
                }
            ],
        )

        instance = launch_template.create_instance(
            name, subnet=subnet, security_group=security_group
        )
        pulumi.export(
            name, {"instance": instance.public_ip.apply(lambda ip: f"ubuntu@{ip}")}
        )

        self.security_group = security_group
        self.instance = instance

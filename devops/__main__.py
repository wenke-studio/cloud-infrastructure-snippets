"""DevOps resources entry point."""

import pulumi
from integrator.aws import ec2

from components.instance import InstanceComponent


def main():
    """Create a runner and monitor instances with dependencies resources."""

    stack = pulumi.get_stack()

    # shared resources
    vpc = ec2.Vpc(stack, cidr_block="10.0.0.0/16")
    key_pair = ec2.KeyPair(stack, public_key="/path/to/public_key.pub")

    # runner
    runner = InstanceComponent(
        "runner", vpc=vpc, cidr_block="10.0.1.0/24", key_pair=key_pair
    )

    # monitor
    monitor = InstanceComponent(
        "monitor", vpc=vpc, cidr_block="10.0.2.0/24", key_pair=key_pair
    )

    # dependencies resources
    runner.security_group.add_ingress_rule(
        "node-exporter",
        port=9100,
        protocol="tcp",
        source_security_group_id=monitor.security_group.id,
    )
    runner.security_group.add_ingress_rule(
        "container-exporter",
        port=8080,
        protocol="tcp",
        source_security_group_id=monitor.security_group.id,
    )


if __name__ == "__main__":
    main()

"""Service resources entry point."""

import pulumi
from integrator.aws import ec2

from components import ElasticsearchComponent


def main():
    """Create service resources."""

    stack = pulumi.get_stack()

    # shared resources
    vpc = ec2.Vpc(stack, cidr_block="10.0.0.0/16")

    # frontend resources

    # backend resources

    ## option 1: ecs task
    # TaskComponent("api", vpc=vpc, cidr_block_index=1)

    ## option 2: api gateway
    # ApiGatewayComponent('api', vpc=vpc, cidr_block_index=2) # todo: TBD

    # storage resources

    ## option 1: elasticsearch
    ElasticsearchComponent("es", vpc=vpc, cidr_block_index=10)

    ## option 2: rds
    # RdsComponent("rds", vpc=vpc, cidr_block_index=11)  # todo: TBD


if __name__ == "__main__":
    main()

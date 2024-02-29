from typing import Optional

from integrator.aws import acm, ec2, opensearch


class ElasticsearchComponent:
    def __init__(
        self,
        name: str,
        vpc: ec2.Vpc,
        cidr_block_index: int,
        instance_count: int = 1,
        instance_type: str = "t3.medium.search",
        volume_size: int = 10,
        endpoint: Optional[str] = None,
        certificate: Optional[acm.Certificate] = None,
    ) -> None:

        subnets = []
        for index, availability_zone in enumerate(vpc.availability_zones):
            subnet = vpc.create_public_subnet(
                name,
                availability_zone=availability_zone,
                cidr_block=f"10.0.{cidr_block_index+index}.0/24",  # cidr_block is defined by vpc
            )
            subnets.append(subnet)

        security_group = vpc.create_security_group(name)

        opensearch.Domain(
            name,
            doamin_name=name,
            subnets=subnets,
            security_group=security_group,
            instance_count=instance_count,
            instance_type=instance_type,
            volume_size=volume_size,
            endpoint=endpoint,
            certificate=certificate,
        )

        self.security_group = security_group

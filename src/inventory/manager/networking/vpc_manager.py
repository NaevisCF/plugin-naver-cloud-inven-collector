from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.networking.vpc_connector import VpcConnector


class VpcManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Networking"
        self.cloud_service_type = "vpc"
        self.metadata_path = "metadata/spaceone/networking/vpc.yaml"

    def collect_resources(self, options, secret_data):
        try:
            yield from self.collect_cloud_service_type()
            yield from self.collect_cloud_service(options, secret_data)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data):
        vpc_connector = VpcConnector(secret_data=secret_data)
        vpc_list = vpc_connector.list_vpc()
        subnet_list = vpc_connector.list_subnet()
        route_table_list = vpc_connector.list_route_table()
        network_acl_list = vpc_connector.list_network_acl()
        nat_gateway_list = vpc_connector.list_nat_gateway_instance()
        vpc_peering_list = vpc_connector.list_vpc_peering_instance()

        for vpc in vpc_list:
            vpc_no = vpc.vpc_no
            matched_subnet_list = self._get_matched_subnet_list(subnet_list, vpc_no)
            matched_route_table_list = self._get_matched_route_table_list(route_table_list, vpc_no)
            matched_network_acl_list = self._get_matched_network_acl_list(network_acl_list, vpc_no)
            matched_nat_gateway_list = self._get_matched_nat_gateway_list(nat_gateway_list, vpc_no)
            matched_vpc_peering_list = self._get_matched_vpc_peering_list(vpc_peering_list, vpc_no)
            
            vpc_data = {
                'vpc_no': vpc_no,
                'ipv4_cidr_block': vpc.ipv4_cidr_block,
                'vpc_status': vpc.vpc_status.code,
                'region_code': vpc.region_code,
                'create_date': vpc.create_date,
                'subnet_list': matched_subnet_list,
                'vpc_peering_list': matched_vpc_peering_list,
                'route_table_list': matched_route_table_list,
                'nat_gateway_instance_list': matched_nat_gateway_list,
                'network_acl_list': matched_network_acl_list
            }

            resource_id = vpc_data["vpc_no"]
            link = ""
            reference = self.get_reference(resource_id, link)

            cloud_service = make_cloud_service(
                name=vpc.vpc_name,
                region_code=vpc.region_code,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                reference=reference,
                provider=self.provider,
                data=vpc_data,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )

    @staticmethod
    def _get_matched_subnet_list(subnet_list, vpc_no):
        subnet_data_list = []
        for subnet in subnet_list:
            if vpc_no == subnet.vpc_no:
                subnet = {
                    'subnet_no': subnet.subnet_no,
                    'zone_code': subnet.zone_code,
                    'subnet_name': subnet.subnet_name,
                    'subnet_status': subnet.subnet_status.code,
                    'create_date': subnet.create_date,
                    'subnet_type': subnet.subnet_type.code,
                    'usage_type': subnet.usage_type.code,
                    'network_acl_no': subnet.network_acl_no,
                }
                subnet_data_list.append(subnet)

        return subnet_data_list

    @staticmethod
    def _get_matched_route_table_list(route_table_list, vpc_no):
        route_table_data_list = []
        for route_table in route_table_list:
            if vpc_no == route_table.vpc_no:
                route_table = {
                    'route_table_name': route_table.route_table_name,
                    'route_table_no': route_table.route_table_no,
                    'is_default': route_table.is_default,
                    'supported_subnet_type': route_table.supported_subnet_type.code,
                    'route_table_status': route_table.route_table_status.code,
                    'route_table_description': route_table.route_table_description,

                }
                route_table_data_list.append(route_table)

        return route_table_data_list

    @staticmethod
    def _get_matched_network_acl_list(network_acl_list, vpc_no):
        network_acl_data_list = []
        for network_acl in network_acl_list:
            if vpc_no == network_acl.vpc_no:
                network_acl = {
                    'network_acl_no': network_acl.network_acl_no,
                    'nat_gateway_name': network_acl.network_acl_name,
                    'network_acl_status': network_acl.network_acl_status.code,
                    'network_acl_description': network_acl.network_acl_description,
                    'is_default': network_acl.is_default,
                }
                network_acl_data_list.append(network_acl)

        return network_acl_data_list

    @staticmethod
    def _get_matched_nat_gateway_list(nat_gateway_list, vpc_no):
        nat_gateway_instance_data_list = []
        for nat_gateway in nat_gateway_list:
            if vpc_no == nat_gateway.vpc_no:
                nat_gateway = {
                    'nat_gateway_instance_no': nat_gateway.nat_gateway_instance_no,
                    'nat_gateway_name': nat_gateway.nat_gateway_name,
                    'public_ip': nat_gateway.public_ip,
                    'nat_gateway_instance_status': nat_gateway.nat_gateway_instance_status.code,
                    'nat_gateway_instance_status_name': nat_gateway.nat_gateway_instance_status_name,
                    'nat_gateway_instance_operation': nat_gateway.nat_gateway_instance_operation.code,
                    'nat_gateway_description': nat_gateway.nat_gateway_description
                }
                nat_gateway_instance_data_list.append(nat_gateway)

        return nat_gateway_instance_data_list

    @staticmethod
    def _get_matched_vpc_peering_list(vpc_peering_list, vpc_no):
        vpc_peering_data_list = []
        for vpc_peering in vpc_peering_list:
            if vpc_no == vpc_peering.vpc_no:
                vpc_peering = {
                    'vpc_peering_instance_no': vpc_peering.vpc_peering_instance_no,
                    'vpc_peering_name': vpc_peering.vpc_peering_name,
                    'last_modify_date': vpc_peering.last_modifiy_date,
                    'vpc_peering_instance_status': vpc_peering.vpc_peering_instance_status.code,
                    'vpc_peering_instance_status_name': vpc_peering.vpc_peering_instance_status_name,
                    'vpc_peering_instance_operation': vpc_peering.vpc_peering_instance_operation.code,
                    'source_vpc_no': vpc_peering.source_vpc_no,
                    'source_vpc_name': vpc_peering.source_vpc_name,
                    'source_vpc_ipv4_cidr_block': vpc_peering.source_vpc_ipv4_cidr_block,
                    'source_vpc_login_id': vpc_peering.source_vpc_login_id,
                    'target_vpc_no': vpc_peering.target_vpc_no,
                    'target_vpc_name': vpc_peering.target_vpc_name,
                    'target_vpc_ipv4_cidr_block': vpc_peering.target_vpc_ipv4_cidr_block,
                    'target_vpc_login_id': vpc_peering.target_vpc_login_id,
                    'vpc_peering_description': vpc_peering.vpc_peering_description,
                    'has_reverse_vpc_peering': vpc_peering.has_reverse_vpc_peering,
                    'is_between_accounts': vpc_peering.is_between_accounts,
                    'reverse_vpc_peering_instance_no': vpc_peering.reverse_vpc_peering_instance_no,
                }
                vpc_peering_data_list.append(vpc_peering)

        return vpc_peering_data_list

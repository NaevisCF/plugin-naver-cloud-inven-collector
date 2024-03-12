import logging
import ncloud_vpc
from spaceone.core.connector import BaseConnector
from ncloud_server.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class VpcConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vpc_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_vpc = ncloud_vpc.Configuration()
        configuration_vpc.access_key = secret_data['ncloud_access_key_id']
        configuration_vpc.secret_key = secret_data['ncloud_secret_key']
        self.vpc_client = ncloud_vpc.V2Api(ncloud_vpc.ApiClient(configuration_vpc))

    def list_vpc(self):
        vpc_list = []
        get_vpc_list_request = ncloud_vpc.GetVpcListRequest()

        try:
            api_response = self.vpc_client.get_vpc_list(get_vpc_list_request)
            for instance in api_response.vpc_list:
                vpc_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_server_instance_list: %s\n" % e)

        return vpc_list

    def list_subnet(self):
        subnet_list = []
        get_subnet_list_request = ncloud_vpc.GetSubnetListRequest()

        try:
            api_response = self.vpc_client.get_subnet_list(get_subnet_list_request)
            for instance in api_response.subnet_list:
                subnet_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_subnet_list: %s\n" % e)

        return subnet_list

    def list_network_acl(self):
        network_acl_list = []
        get_network_acl_list_request = ncloud_vpc.GetNetworkAclListRequest()

        try:
            api_response = self.vpc_client.get_network_acl_list(get_network_acl_list_request)
            for instance in api_response.network_acl_list:
                network_acl_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_network_acl_list: %s\n" % e)

        return network_acl_list

    def list_nat_gateway_instance(self):
        nat_gateway_instance_list = []
        get_nat_gateway_instance_list_request = ncloud_vpc.GetNatGatewayInstanceListRequest()

        try:
            api_response = self.vpc_client.get_nat_gateway_instance_list(get_nat_gateway_instance_list_request)
            for instance in api_response.nat_gateway_instance_list:
                nat_gateway_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_nat_gateway_instance_list_request: %s\n" % e)

        return nat_gateway_instance_list

    def list_vpc_peering_instance(self):
        vpc_peering_instance_list = []
        get_vpc_peering_instance_list_request = ncloud_vpc.GetVpcPeeringInstanceListRequest()

        try:
            api_response = self.vpc_client.get_vpc_peering_instance_list(get_vpc_peering_instance_list_request)
            for instance in api_response.vpc_peering_instance_list:
                vpc_peering_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_vpc_peering_instance_list_request: %s\n" % e)

        return vpc_peering_instance_list

    def list_route_table(self):
        route_table_list = []
        get_route_table_list_request = ncloud_vpc.GetRouteTableListRequest()

        try:
            api_response = self.vpc_client.get_route_table_list(get_route_table_list_request)
            for instance in api_response.route_table_list:
                route_table_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_route_table_list: %s\n" % e)

        return route_table_list

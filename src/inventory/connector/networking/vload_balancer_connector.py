import logging
import ncloud_vloadbalancer
from spaceone.core.connector import BaseConnector
from ncloud_vserver.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class VLoadBalancerConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vloadbalancer_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_vloadbalancer = ncloud_vloadbalancer.Configuration()
        configuration_vloadbalancer.access_key = secret_data['ncloud_access_key_id']
        configuration_vloadbalancer.secret_key = secret_data['ncloud_secret_key']
        self.vloadbalancer_client = ncloud_vloadbalancer.V2Api(ncloud_vloadbalancer.ApiClient(configuration_vloadbalancer))

    def list_vload_balancer_instance(self):
        vload_balancer_list = []
        get_vload_balancer_instance_list_request = ncloud_vloadbalancer.GetLoadBalancerInstanceListRequest()

        try:
            api_response = self.vloadbalancer_client.get_load_balancer_instance_list(get_vload_balancer_instance_list_request)
            for instance in api_response.load_balancer_instance_list:
                vload_balancer_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_vload_balancer_instance_list: %s\n" % e)

        return vload_balancer_list

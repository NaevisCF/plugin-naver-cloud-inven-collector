import logging

import ncloud_loadbalancer
import ncloud_vpc
from spaceone.core.connector import BaseConnector
from ncloud_server.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class LoadBalancerConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loadbalancer_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_loadbalancer = ncloud_loadbalancer.Configuration()
        configuration_loadbalancer.access_key = secret_data['ncloud_access_key_id']
        configuration_loadbalancer.secret_key = secret_data['ncloud_secret_key']
        self.loadbalancer_client = ncloud_loadbalancer.V2Api(ncloud_loadbalancer.ApiClient(configuration_loadbalancer))

    def list_load_balancer_instance(self):
        load_balancer_list = []
        get_load_balancer_instance_list_request = ncloud_loadbalancer.GetLoadBalancerInstanceListRequest()

        try:
            api_response = self.loadbalancer_client.get_load_balancer_instance_list(get_load_balancer_instance_list_request)
            for instance in api_response.load_balancer_instance_list:
                load_balancer_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_load_balancer_instance_list: %s\n" % e)

        return load_balancer_list


    # ssl 인증서 비밀키, 공개키까지 가져와야 하는지 확인
    # def list_load_balancer_ssl_certificate(self):
    #     ssl_certificate_list = []
    #     get_load_balancer_ssl_certificate_list_request = ncloud_loadbalancer.GetLoadBalancerSslCertificateListRequest()
    #
    #     try:
    #         api_response = self.loadbalancer_client.get_load_balancer_ssl_certificate_list(get_load_balancer_ssl_certificate_list_request)
    #         for certificate in api_response:
    #             ssl_certificate_list.append(certificate)
    #
    #     except ApiException as e:
    #         print("Exception when calling V2Api->get_load_balancer_ssl_certificate_list: %s\n" % e)
    #
    #     return ssl_certificate_list




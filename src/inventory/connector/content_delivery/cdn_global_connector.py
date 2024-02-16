import logging
import ncloud_cdn
from spaceone.core.connector import BaseConnector
from ncloud_server.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class CdnGlobalConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cdn_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_cdn = ncloud_cdn.Configuration()
        configuration_cdn.access_key = secret_data['ncloud_access_key_id']
        configuration_cdn.secret_key = secret_data['ncloud_secret_key']
        self.cdn_client = ncloud_cdn.V2Api(ncloud_cdn.ApiClient(configuration_cdn))

    def list_cdn_global_cdn_instance_instance(self):

        global_cdn_instance_list = []
        get_global_cdn_instance_list_request = ncloud_cdn.GetGlobalCdnInstanceListRequest()

        try:
            api_response = self.cdn_client.get_global_cdn_instance_list(get_global_cdn_instance_list_request)
            for instance in api_response.global_cdn_instance_list:
                global_cdn_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_global_cdn_instance_list: %s\n" % e)

        return global_cdn_instance_list

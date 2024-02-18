import logging
import ncloud_cdn
from spaceone.core.connector import BaseConnector
from ncloud_server.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class CdnPlusConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cdn_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_cdn = ncloud_cdn.Configuration()
        configuration_cdn.access_key = secret_data['ncloud_access_key_id']
        configuration_cdn.secret_key = secret_data['ncloud_secret_key']
        self.cdn_client = ncloud_cdn.V2Api(ncloud_cdn.ApiClient(configuration_cdn))

    def list_cdn_plus_instance(self):

        cdn_plus_instance_list = []
        get_cdn_plus_instance_list_request = ncloud_cdn.GetCdnPlusInstanceListRequest()

        try:
            api_response = self.cdn_client.get_cdn_plus_instance_list(get_cdn_plus_instance_list_request)
            # print(api_response)
            for instance in api_response.cdn_plus_instance_list:
                cdn_plus_instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cdn_plus_instance_list: %s\n" % e)

        return cdn_plus_instance_list

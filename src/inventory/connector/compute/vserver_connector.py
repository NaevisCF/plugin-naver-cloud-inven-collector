import logging
import ncloud_vserver
from spaceone.core.connector import BaseConnector
from ncloud_vserver.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class VServerConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_vserver = ncloud_vserver.Configuration()
        configuration_vserver.access_key = secret_data['ncloud_access_key_id']
        configuration_vserver.secret_key = secret_data['ncloud_secret_key']
        self.server_client = ncloud_vserver.V2Api(ncloud_vserver.ApiClient(configuration_vserver))

    def list_server_instance(self):

        instance_list = []
        get_server_instance_list_request = ncloud_vserver.GetServerInstanceListRequest()

        try:
            api_response = self.server_client.get_server_instance_list(get_server_instance_list_request)
            for instance in api_response.server_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_vserver_instance_list: %s\n" % e)

        return instance_list

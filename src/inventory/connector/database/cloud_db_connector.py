import logging
import ncloud_clouddb
from spaceone.core.connector import BaseConnector
from ncloud_server.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class CloudDBConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_db_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_cloud_db = ncloud_clouddb.Configuration()
        configuration_cloud_db.access_key = secret_data['ncloud_access_key_id']
        configuration_cloud_db.secret_key = secret_data['ncloud_secret_key']
        self.cloud_db_client = ncloud_clouddb.V2Api(ncloud_clouddb.ApiClient(configuration_cloud_db))

    def list_cloud_db_instance(self, db_kind_code):

        instance_list = []
        get_cloud_db_instance_list_request = ncloud_clouddb.GetCloudDBInstanceListRequest(db_kind_code=db_kind_code)

        try:
            api_response = self.cloud_db_client.get_cloud_db_instance_list(get_cloud_db_instance_list_request)
            for instance in api_response.cloud_db_instance_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_cloud_db_instance_list: %s\n" % e)

        return instance_list

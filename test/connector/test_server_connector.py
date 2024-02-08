import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase

from spaceone_ncloud.connector.compute.server_connector import ServerConnector

_LOGGER = logging.getLogger(__name__)


class TestServerConnector(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    server_connector = ServerConnector(secret_data=secrets)

    def test_list_server_instance(self):
        server_instances = self.server_connector.list_server_instance()

        print(server_instances)

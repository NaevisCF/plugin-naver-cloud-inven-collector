import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase
from spaceone_company.manager.compute.server_manager import ServerManager

_LOGGER = logging.getLogger(__name__)


class TestServerManager(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    server_manager = ServerManager(secret_data=secrets)
    server_instances = server_manager.collect_cloud_service(options={}, secret_data=secrets, schema={})

    for server_instance in server_instances:
        print(server_instance)


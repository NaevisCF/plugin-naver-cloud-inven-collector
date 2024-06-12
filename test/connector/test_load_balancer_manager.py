import os
import logging
from spaceone.core import utils
from spaceone.tester import TestCase
from inventory.connector.networking.load_balancer_connector import LoadBalancerConnector
from inventory.connector.networking.vload_balancer_connector import VLoadBalancerConnector

_LOGGER = logging.getLogger(__name__)


class TestLoadBalancerConnector(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    load_balancer_connector = LoadBalancerConnector(secret_data=secrets)
    vload_balancer_connector = VLoadBalancerConnector(secret_data=secrets)

    def test_list_load_balancer_instance(self):
        load_balancer_instances = self.load_balancer_connector.list_load_balancer_instance()

        print(load_balancer_instances)

    def test_list_vload_balancer_instance(self):
        vload_balancer_instances = self.vload_balancer_connector.list_vload_balancer_instance()

        print(vload_balancer_instances)

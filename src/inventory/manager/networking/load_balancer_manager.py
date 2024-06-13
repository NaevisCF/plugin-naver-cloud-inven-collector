from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.networking.load_balancer_connector import LoadBalancerConnector


class LoadBalancerManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Networking"
        self.cloud_service_type = "Load Balancer"
        self.metadata_path = "metadata/spaceone/networking/load_balancer.yaml"

    def create_cloud_service_type(self):
        result = []
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        result.append(cloud_service_type)
        return result

    def create_cloud_service(self, options, secret_data):
        loadbalancer_connector = LoadBalancerConnector(secret_data=secret_data)
        loadbalancer_list = loadbalancer_connector.list_load_balancer_instance()

        for loadbalancer in loadbalancer_list:
            try:
                load_balancer_name = loadbalancer.load_balancer_name
                load_balancer_rule_list = self._get_load_balancer_rule_list(loadbalancer.load_balancer_rule_list)
                load_balanced_server_instance_list = self._get_load_balanced_server_instance_list(loadbalancer.load_balanced_server_instance_list)

                loadbalancer_data = {
                    'load_balancer_instance_no': loadbalancer.load_balancer_instance_no,
                    'virtual_ip': loadbalancer.virtual_ip,
                    'load_balancer_algorithm_type': loadbalancer.load_balancer_algorithm_type.code_name,
                    'load_balancer_description': loadbalancer.load_balancer_description,
                    'create_date': loadbalancer.create_date,
                    'domain_name': loadbalancer.domain_name,
                    'internet_line_type': loadbalancer.internet_line_type.code_name,
                    'load_balancer_instance_status_name': loadbalancer.load_balancer_instance_status_name,
                    'load_balancer_instance_status': loadbalancer.load_balancer_instance_status.code_name,
                    'load_balancer_instance_operation': loadbalancer.load_balancer_instance_operation.code_name,
                    'network_usage_type': loadbalancer.network_usage_type.code_name,
                    'is_http_keep_alive': loadbalancer.is_http_keep_alive,
                    'connection_timeout': loadbalancer.connection_timeout,
                    'certificate_name': loadbalancer.certificate_name,
                    'load_balancer_rule_list': load_balancer_rule_list,
                    'load_balanced_server_instance_list': load_balanced_server_instance_list
                }

                link = ""
                resource_id = load_balancer_name
                reference = self.get_reference(resource_id, link)

                cloud_service = make_cloud_service(
                    name=load_balancer_name,
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=loadbalancer_data,
                    reference=reference
                )
                yield cloud_service

            except Exception as e:
                _LOGGER.error(
                    f'[list_instances] [{loadbalancer.load_balancer_instance_no}] {e}'
                )
                yield make_error_response(
                    error=e,
                    provider=self.provider,
                    cloud_service_group=self.cloud_service_group,
                    cloud_service_type=self.cloud_service_type,
                )

    @staticmethod
    def _get_load_balancer_rule_list(load_balancer_rule_list):
        load_balancer_rule_list_info = []

        for load_balancer_rule in load_balancer_rule_list:
            info = {
                'protocol_type': load_balancer_rule.protocol_type.code_name,
                'load_balancer_port': load_balancer_rule.load_balancer_port,
                'server_port': load_balancer_rule.server_port,
                'l7_health_check_path': load_balancer_rule.l7_health_check_path,
                'certificate_name': load_balancer_rule.certificate_name,
                'proxy_protocol_use_yn': load_balancer_rule.proxy_protocol_use_yn
            }

            load_balancer_rule_list_info.append(info)

        return load_balancer_rule_list_info

    # 서버 정보를 전부 가져와야 하는지 확인
    @staticmethod
    def _get_load_balanced_server_instance_list(load_balanced_server_instance_list):
        load_balanced_server_instance_list_info = []

        for load_balanced_server_instance in load_balanced_server_instance_list:
            info = {
                'server_instance_no': load_balanced_server_instance.server_instance.server_instance_no,
                'server_name': load_balanced_server_instance.server_instance.server_name,
                'server_description': load_balanced_server_instance.server_instance.server_description
            }

            load_balanced_server_instance_list_info.append(info)

        return load_balanced_server_instance_list_info

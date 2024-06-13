from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.networking.vload_balancer_connector import VLoadBalancerConnector


class VLoadBalancerManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Networking"
        self.cloud_service_type = "VLoad Balancer"
        self.metadata_path = "metadata/spaceone/networking/vload_balancer.yaml"

    def create_cloud_service_type(self):
        result = []
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            service_code="NCloud_VloadBalancer",
            labels=["Networking", "VloadBalancer"]
        )
        result.append(cloud_service_type)
        return result

    def create_cloud_service(self, options, secret_data):
        vloadbalancer_connector = VLoadBalancerConnector(secret_data=secret_data)
        vloadbalancer_list = vloadbalancer_connector.list_vload_balancer_instance()

        for vloadbalancer in vloadbalancer_list:
            try:
                vload_balancer_name = vloadbalancer.load_balancer_name
                vload_balancer_ip_list = self._get_vload_balancer_ip_list(vloadbalancer.load_balancer_ip_list)
                subnet_no_list = self._get_subnet_no_list(vloadbalancer.subnet_no_list)
                vload_balancer_listener_no_list = self._get_vload_balancer_listener_no_list(
                    vloadbalancer.load_balancer_listener_no_list)

                vloadbalancer_data = {
                    'create_date': vloadbalancer.create_date,
                    'idle_timeout': vloadbalancer.idle_timeout,
                    'load_balancer_description': vloadbalancer.load_balancer_description,
                    'load_balancer_domain': vloadbalancer.load_balancer_domain,
                    'load_balancer_instance_no': vloadbalancer.load_balancer_instance_no,
                    'load_balancer_instance_operation': vloadbalancer.load_balancer_instance_operation.code,
                    'load_balancer_instance_status': vloadbalancer.load_balancer_instance_status.code,
                    'load_balancer_instance_status_name': vloadbalancer.load_balancer_instance_status_name,
                    'load_balancer_ip_list': vload_balancer_ip_list,
                    'load_balancer_listener_no_list': vload_balancer_listener_no_list,
                    'load_balancer_name': vloadbalancer.load_balancer_name,
                    'load_balancer_network_type': vloadbalancer.load_balancer_network_type.code,
                    'load_balancer_type': vloadbalancer.load_balancer_type.code,
                    'region_code': vloadbalancer.region_code,
                    'subnet_no_list': subnet_no_list,
                    'throughput_type': vloadbalancer.throughput_type.code,
                    'vpc_no': vloadbalancer.vpc_no
                }

                link = ""
                resource_id = vloadbalancer_data.get('load_balancer_instance_no')
                reference = self.get_reference(resource_id, link)

                cloud_service = make_cloud_service(
                    name=vload_balancer_name,
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    reference=reference,
                    data=vloadbalancer_data,
                    region_code=vloadbalancer_data.get('region_code')
                )
                yield cloud_service

            except Exception as e:
                _LOGGER.error(
                    f'[list_instances] [{vloadbalancer.load_balancer_instance_no}] {e}'
                )
                yield make_error_response(
                    error=e,
                    provider=self.provider,
                    cloud_service_group=self.cloud_service_group,
                    cloud_service_type=self.cloud_service_type,
                )

    @staticmethod
    def _get_vload_balancer_ip_list(vload_balancer_ip_list):
        vload_balancer_ip_list_info = []

        for vload_balancer_ip in vload_balancer_ip_list:
            info = {
                'load_balancer_ip_list': vload_balancer_ip
            }

            vload_balancer_ip_list_info.append(info)

        return vload_balancer_ip_list_info

    @staticmethod
    def _get_subnet_no_list(subnet_no_list):
        subnet_no_list_info = []

        for subnet_no in subnet_no_list:
            info = {
                'subnet_no_list': subnet_no
            }

            subnet_no_list_info.append(info)

        return subnet_no_list_info

    @staticmethod
    def _get_vload_balancer_listener_no_list(vload_balancer_listener_no_list):
        vload_balancer_listener_no_list_info = []

        for vload_balancer_listener_no in vload_balancer_listener_no_list:
            info = {
                'load_balancer_listener_no_list': vload_balancer_listener_no
            }

            vload_balancer_listener_no_list_info.append(info)

        return vload_balancer_listener_no_list_info

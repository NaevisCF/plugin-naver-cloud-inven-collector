import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from spaceone_company.connector.compute.server_connector import ServerConnector

_LOGGER = logging.getLogger("cloudforet")


def get_compute_data(instance):
    compute_data = {
        'server_instance_no': instance.server_instance_no,
        'server_image_name': instance.server_image_name,
        'server_instance_status': instance.server_instance_status.code,
        'server_instance_operation': instance.server_instance_operation.code,
        'server_instance_status_name': instance.server_instance_status_name,
        'platform_type': instance.platform_type.code_name,
        'create_date': instance.create_date,
        'uptime': instance.uptime,
        'server_image_product_code': instance.server_image_product_code,
        'server_product_code': instance.server_product_code,
        'server_instance_type': instance.server_instance_type.code,
        'zone': instance.zone.zone_name
    }
    return compute_data


def get_hardware_data(instance):
    hardware_data = {
        'cpu_count': instance.cpu_count,
        'memory_size': instance.memory_size
    }
    return hardware_data


def get_port_forwarding_rules_data(instance):
    port_forwarding_rules_data = {
        'port_forwarding_external_port': instance.port_forwarding_external_port,
        'port_forwarding_internal_port': instance.port_forwarding_internal_port,
        'port_forwarding_public_ip': instance.port_forwarding_public_ip
    }
    return port_forwarding_rules_data


def get_ip_data(instance):
    ip_data = {
        'private_ip': instance.private_ip,
        'public_ip': instance.public_ip
    }
    return ip_data


class ServerManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "SpaceONE"
        self.cloud_service_type = "Server"
        self.provider = "naver cloud"
        self.metadata_path = "metadata/spaceone/compute.yaml"

    def collect_resources(self, options, secret_data, schema):
        try:
            yield from self.collect_cloud_service_type(options, secret_data, schema)
            yield from self.collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data, schema):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data, schema):
        server_connector = ServerConnector(secret_data=secret_data)
        server_instances = server_connector.list_server_instance()
        for server_instance in server_instances:
            compute_data = get_compute_data(server_instance)
            hardware_data = get_hardware_data(server_instance)
            port_forwarding_rules_data = get_port_forwarding_rules_data(server_instance)
            ip_data = get_ip_data(server_instance)

            server_data = {
                'compute': compute_data,
                'hardware': hardware_data,
                'port_forwarding_rules': port_forwarding_rules_data,
                'ip': ip_data
            }

            cloud_service = make_cloud_service(
                name=server_instance.server_name,
                instance_type=server_instance.server_instance_type.code,
                region_code=server_instance.region.region_name,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=server_data,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )

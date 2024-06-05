from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.compute.vserver_connector import VServerConnector


class VServerManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Compute"
        self.cloud_service_type = "VServer"
        self.metadata_path = "metadata/spaceone/compute/vserver.yaml"

    def collect_resources(self, options, secret_data):
        try:
            yield from self.collect_cloud_service_type(options, secret_data)
            yield from self.collect_cloud_service(options, secret_data)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data):
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
            match_keys=[["name", "group", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data):
        vserver_connector = VServerConnector(secret_data=secret_data)
        server_instances = vserver_connector.list_server_instance()
        for server_instance in server_instances:
            compute_data = self._get_compute_data(server_instance)
            hardware_data = self._get_hardware_data(server_instance)
            network_data = self._get_network_data(server_instance)

            server_data = {
                'compute': compute_data,
                'hardware': hardware_data,
                'network': network_data
            }

            resource_id = server_data["compute"]["server_instance_no"]
            link = server_data["compute"]["server_instance_no"]
            reference = self.get_reference(resource_id, link)

            cloud_service = make_cloud_service(
                name=server_instance.server_name,
                instance_type=server_instance.server_instance_type.code,
                region_code=server_instance.region_code,
                reference=reference,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=server_data,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["cloud_service_type", "cloud_service_group", "reference.resource_id", "provider"]],
                resource_type="inventory.CloudService"
            )

    @staticmethod
    def _get_compute_data(instance):
        compute_data = {
            'server_instance_no': instance.server_instance_no,
            'server_name': instance.server_name,
            'server_description': instance.server_description,
            'server_instance_status': instance.server_instance_status.code,
            'server_instance_operation': instance.server_instance_operation.code,
            'server_instance_status_name': instance.server_instance_status_name,
            'platform_type': instance.platform_type.code_name,
            'create_date': instance.create_date,
            'uptime': instance.uptime,
            'server_image_product_code': instance.server_image_product_code,
            'server_product_code': instance.server_product_code,
            'server_instance_type': instance.server_instance_type.code,
            'zone_code': instance.zone_code
        }
        return compute_data

    @staticmethod
    def _get_hardware_data(instance):
        hardware_data = {
            'cpu_count': instance.cpu_count,
            'memory_size': round((instance.memory_size / (1024 * 1024 * 1024)), 2),
            'base_block_storage_disk_type': instance.base_block_storage_disk_type.code_name,
            'base_block_storage_disk_detail_type': instance.base_block_storage_disk_detail_type.code_name
        }
        return hardware_data

    @staticmethod
    def _get_network_data(instance):
        network_data = {
            'vpc_no': instance.vpc_no,
            'subnet_no': instance.subnet_no,
            'public_ip_instance_no': instance.public_ip_instance_no,
            'public_ip': instance.public_ip
        }
        return network_data

from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.database.cloud_db_connector import CloudDBConnector


class CloudDBManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Database"
        self.cloud_service_type = "Cloud DB"
        self.metadata_path = "metadata/spaceone/database/cloud_db.yaml"

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
        cloud_db_connector = CloudDBConnector(secret_data=secret_data)
        cloud_db_instances = cloud_db_connector.list_cloud_db_instance(options.get("db_kind_code", {}))

        for instance in cloud_db_instances:
            try:
                cloud_db_service_name = instance.cloud_db_service_name
                cloud_db_create_date = instance.create_date
                zone = self._get_zone(instance.zone)
                region = self._get_region(instance.region)
                cloud_db_config_list = self._get_cloud_db_config_list(instance.cloud_db_config_list)
                cloud_db_config_group_list = self._get_cloud_db_config_group_list(instance.cloud_db_config_group_list)
                access_control_group_list = self._get_access_control_group_list(instance.access_control_group_list)
                cloud_db_server_instance_list = self._get_cloud_db_server_instance_list(instance.cloud_db_server_instance_list)

                instance_data = {
                    'cloud_db_create_date': cloud_db_create_date,
                    'cloud_db_instance_no': instance.cloud_db_instance_no,
                    'db_kind_code': instance.db_kind_code,
                    'cpu_count': instance.cpu_count,
                    'engine_version': instance.engine_version,
                    'data_storage_type': instance.data_storage_type.code_name,
                    'license_code': instance.license_code,
                    'is_ha': instance.is_ha,
                    'cloud_db_port': instance.cloud_db_port,
                    'backup_time': instance.backup_time,
                    'backup_file_retention_period': instance.backup_file_retention_period,
                    'cloud_db_instance_status_name': instance.cloud_db_instance_status_name,
                    'zone': zone,
                    'region': region,
                    'cloud_db_config_list': cloud_db_config_list,
                    'cloud_db_config_group_list': cloud_db_config_group_list,
                    'access_control_group_list': access_control_group_list,
                    'cloud_db_server_instance_list': cloud_db_server_instance_list,
                }

                link = ""
                resource_id = instance.get('cloud_db_instance_no')
                reference = self.get_reference(resource_id, link)

                cloud_service = make_cloud_service(
                    name=cloud_db_service_name,
                    instance_type=instance.server_instance_type.code,
                    region_code=instance.region.region_code,
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    reference=reference,
                    data=instance_data,
                )
                yield cloud_service

            except Exception as e:
                _LOGGER.error(
                    f'[list_instances] [{instance.cloud_db_instance_no}] {e}'
                )
                yield make_error_response(
                    error=e,
                    provider=self.provider,
                    cloud_service_group=self.cloud_service_group,
                    cloud_service_type=self.cloud_service_type,
                )

    @staticmethod
    def _get_zone(zone):
        zone_info = {
                'zone_description': zone.zone_description,
                'zone_name': zone.zone_name,
                'zone_no': zone.zone_no
            }

        return zone_info

    @staticmethod
    def _get_region(region):
        region_info = {
                'region_no': region.region_no,
                'region_code': region.region_code,
                'region_name': region.region_name
            }

        return region_info

    @staticmethod
    def _get_cloud_db_config_list(cloud_db_config_list):
        cloud_db_config_list_info = []

        for cloud_db_config in cloud_db_config_list:
            info = {
                'config_name': cloud_db_config.config_name,
                'config_value': cloud_db_config.config_value
            }

            cloud_db_config_list_info.append(info)

        return cloud_db_config_list_info

    @staticmethod
    def _get_cloud_db_config_group_list(cloud_db_config_group_list):
        cloud_db_config_group_list_info = []

        for cloud_db_config_group in cloud_db_config_group_list:
            info = {
                'config_group_name': cloud_db_config_group.config_group_name,
                'config_group_type': cloud_db_config_group.config_group_type,
                'config_group_no': cloud_db_config_group.config_group_no
            }

            cloud_db_config_group_list_info.append(info)

        return cloud_db_config_group_list_info

    @staticmethod
    def _get_access_control_group_list(access_control_group_list):
        access_control_group_list_info = []

        for access_control_group in access_control_group_list:
            info = {
                'access_control_group_configuration_no': access_control_group.access_control_group_configuration_no,
                'access_control_group_name': access_control_group.access_control_group_name,
                'access_control_group_description': access_control_group.access_control_group_description,
                'is_default': access_control_group.is_default,
                'create_date': access_control_group.create_date
            }

            access_control_group_list_info.append(info)

        return access_control_group_list_info

    @staticmethod
    def _get_cloud_db_server_instance_list(cloud_db_server_instance_list):
        cloud_db_server_instance_list_info = []

        for cloud_db_server_instance in cloud_db_server_instance_list:
            info = {
                'cloud_db_server_instance_no': cloud_db_server_instance.cloud_db_server_instance_no,
                'cloud_db_server_instance_status_name': cloud_db_server_instance.cloud_db_server_instance_status_name,
                'cloud_db_server_name': cloud_db_server_instance.cloud_db_server_instance_name,
                'cloud_db_server_role': cloud_db_server_instance.cloud_db_server_role.code_name,
                'private_dns_name': cloud_db_server_instance.private_dns_name,
                'public_dns_name': cloud_db_server_instance.public_dns_name,
                'data_storage_size': cloud_db_server_instance.data_storage_size,
                'used_data_storage_size': cloud_db_server_instance.used_data_storage_size,
                'create_date': cloud_db_server_instance.create_date,
                'uptime': cloud_db_server_instance.uptime
            }

            cloud_db_server_instance_list_info.append(info)

        return cloud_db_server_instance_list

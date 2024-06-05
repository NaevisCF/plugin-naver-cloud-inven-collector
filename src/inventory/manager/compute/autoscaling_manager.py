from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.compute.autoscaling_connector import AutoscalingConnector


class AutoscalingManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Compute"
        self.cloud_service_type = "Autoscaling"
        self.metadata_path = "metadata/spaceone/compute/autoscaling.yaml"

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
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data):
        autoscaling_connector = AutoscalingConnector(secret_data=secret_data)
        autoscaling_groups = autoscaling_connector.list_autoscaling_group()
        activity_log_list = autoscaling_connector.list_autoscaling_activity_log()
        configuration_log_list = autoscaling_connector.list_autoscaling_configuration_log()
        launch_configuration_list = autoscaling_connector.list_launch_configuration()

        for autoscaling_group in autoscaling_groups:
            autoscaling_group_name = autoscaling_group.auto_scaling_group_name
            launch_configuration_name = autoscaling_group.launch_configuration_name
            zone_list = self._get_zone_list(autoscaling_group.zone_list)
            matched_activity_log_list = self._get_matched_activity_log_list(activity_log_list, autoscaling_group_name)
            matched_configuration_log_list = self._get_matched_configuration_log_list(configuration_log_list,
                                                                                      autoscaling_group_name)
            matched_launch_configuration_list = self._get_matched_launch_configuration_list(
                launch_configuration_list, launch_configuration_name)

            autoscaling_data = {
                "autoscaling_group_name": autoscaling_group_name,
                'launched_at': autoscaling_group.create_date,
                'default_cooldown': autoscaling_group.default_cooldown,
                'desired_capacity': autoscaling_group.desired_capacity,
                'health_check_grace_period': autoscaling_group.health_check_grace_period,
                'health_check_type': autoscaling_group.health_check_type.code,
                'max_size': autoscaling_group.max_size,
                'min_size': autoscaling_group.min_size,
                'zone_list': zone_list,
                'activity_log_list': matched_activity_log_list,
                'configuration_log_list': matched_configuration_log_list,
                'launch_configuration_list': matched_launch_configuration_list
            }

            cloud_service = make_cloud_service(
                name=autoscaling_group_name,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=autoscaling_data,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )

    @staticmethod
    def _get_zone_list(zone_list):
        zone_list_info = []

        for zone in zone_list:
            zone = {
                'zone_description': zone.zone_description,
                'zone_name': zone.zone_name,
                'zone_no': zone.zone_no
            }
        zone_list_info.append(zone)

        return zone_list_info

    @staticmethod
    def _get_matched_activity_log_list(activity_log_list, autoscaling_group):
        activity_log_list_info = []

        for activity_log in activity_log_list:
            if autoscaling_group == activity_log.auto_scaling_group_name:
                activity_log = {
                    'activity_no': activity_log.activity_no,
                    'description': activity_log.description,
                    'details': activity_log.details,
                    'start_time': activity_log.start_time,
                    'end_time': activity_log.end_time,
                    'status': activity_log.status.code
                }
                activity_log_list_info.append(activity_log)

        return activity_log_list_info

    @staticmethod
    def _get_matched_launch_configuration_list(configuration_log_list, autoscaling_group):
        configuration_log_list_info = []

        for configuration_log in configuration_log_list:
            if autoscaling_group == configuration_log.auto_scaling_group_name:
                configuration_log = {
                    'configuration_action_name': configuration_log.configuration_action_name,
                    'configuration_no': configuration_log.configuration_no,
                    'launch_configuration_name': configuration_log.launch_configuration_name,
                    'scheduled_action_name': configuration_log.scheduled_action_name,
                    'setting_time': configuration_log.setting_time
                }
                configuration_log_list_info.append(configuration_log)

        return configuration_log_list_info

    @staticmethod
    def _get_matched_configuration_log_list(launch_configuration_list, launch_configuration_name):
        launch_configuration_list_info = []
        matched_access_control_group_list = []

        for launch_configuration in launch_configuration_list:
            for access_control_group in launch_configuration.access_control_group_list:
                access_control_group = {
                    'access_control_group_configuration_no': access_control_group.access_control_group_configuration_no,
                    'access_control_group_description': access_control_group.access_control_group_description,
                    'access_control_group_name': access_control_group.access_control_group_name,
                    'is_default_group': access_control_group.is_default_group
                }
                matched_access_control_group_list.append(access_control_group)

            if launch_configuration_name == launch_configuration.launch_configuration_name:
                launch_configuration = {
                    'launch_configuration_name': launch_configuration.launch_configuration_name,
                    'login_key_name': launch_configuration.login_key_name,
                    'access_control_group_list': matched_access_control_group_list
                }
                launch_configuration_list_info.append(launch_configuration)

        return launch_configuration_list_info



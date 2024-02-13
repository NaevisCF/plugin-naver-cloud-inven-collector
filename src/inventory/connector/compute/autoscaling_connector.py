import logging

import ncloud_autoscaling
from spaceone.core.connector import BaseConnector
from ncloud_server.rest import ApiException

_LOGGER = logging.getLogger("cloudforet")


class AutoscalingConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autoscaling_client = None
        self.set_connection(kwargs['secret_data'])

    def set_connection(self, secret_data):
        configuration_autoscaling = ncloud_autoscaling.Configuration()
        configuration_autoscaling.access_key = secret_data['ncloud_access_key_id']
        configuration_autoscaling.secret_key = secret_data['ncloud_secret_key']
        self.autoscaling_client = ncloud_autoscaling.V2Api(ncloud_autoscaling.ApiClient(configuration_autoscaling))

    def list_autoscaling_group(self):

        instance_list = []
        get_auto_scaling_group_list_request = ncloud_autoscaling.GetAutoScalingGroupListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_group_list(get_auto_scaling_group_list_request)
            for instance in api_response.auto_scaling_group_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_group_list: %s\n" % e)

        return instance_list

    def list_autoscaling_activity_log(self):

        instance_list = []
        get_auto_scaling_activity_log_list_request = ncloud_autoscaling.GetAutoScalingActivityLogListRequest()
        try:
            api_response = self.autoscaling_client.get_auto_scaling_activity_log_list(get_auto_scaling_activity_log_list_request)
            for instance in api_response.activity_log_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_activity_log_list: %s\n" % e)

        return instance_list

    def list_autoscaling_configuration_log(self):

        instance_list = []
        get_auto_scaling_configuration_log_list_request = ncloud_autoscaling.GetAutoScalingConfigurationLogListRequest()

        try:
            api_response = self.autoscaling_client.get_auto_scaling_configuration_log_list(get_auto_scaling_configuration_log_list_request)
            for instance in api_response.configuration_log_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_auto_scaling_configuration_log_list: %s\n" % e)

        return instance_list

    def list_launch_configuration(self):

        instance_list = []
        get_launch_configuration_list_request = ncloud_autoscaling.GetLaunchConfigurationListRequest()

        try:
            api_response = self.autoscaling_client.get_launch_configuration_list(get_launch_configuration_list_request)
            for instance in api_response.launch_configuration_list:
                instance_list.append(instance)

        except ApiException as e:
            print("Exception when calling V2Api->get_launch_configuration_list: %s\n" % e)

        return instance_list



from ..base import ResourceManager, _LOGGER
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.content_delivery.cdn_global_connector import CdnGlobalConnector


class CdnGlobalManager(ResourceManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Content Delivery"
        self.cloud_service_type = "Cdn Global"
        self.metadata_path = "metadata/spaceone/content_delivery/cdn_global.yaml"

    def create_cloud_service_type(self):
        result = []
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            labels=["Content Delivery", "CDN Global"]
        )
        result.append(cloud_service_type)
        return result

    def create_cloud_service(self, options, secret_data):
        cdn_connector = CdnGlobalConnector(secret_data=secret_data)
        cdn_instances = cdn_connector.list_cdn_global_cdn_instance_instance()

        for instance in cdn_instances:
            try:
                instance_name = instance.service_name
                global_cdn_service_domain_list = self._get_global_cdn_service_domain_list(instance.global_cdn_service_domain_list)
                global_cdn_rule = self._get_global_cdn_rule(instance.global_cdn_rule)

                instance_data = {
                    'cdn_instance_no': instance.cdn_instance_no,
                    'cdn_instance_status': instance.cdn_instance_status.code_name,
                    'cdn_instance_operation': instance.cdn_instance_operation.code_name,
                    'cdn_instance_status_name': instance.cdn_instance_status_name,
                    'create_date': instance.create_date,
                    'last_modified_date': instance.last_modified_date,
                    'cdn_instance_description': instance.cdn_instance_description,
                    'is_available_partial_domain_purge': instance.is_available_partial_domain_purge,
                    'global_cdn_service_domain_list': global_cdn_service_domain_list,
                    'global_cdn_rule': global_cdn_rule
                }

                link = ""
                resource_id = instance.get('cdn_instance_no')
                reference = self.get_reference(resource_id, link)

                cloud_service = make_cloud_service(
                    name=instance_name,
                    instance_type=instance.server_instance_type.code,
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    reference=reference,
                    data=instance_data
                )
                yield cloud_service

            except Exception as e:
                _LOGGER.error(
                    f'[list_instances] [{instance.cdn_instance_no}] {e}'
                )
                yield make_error_response(
                    error=e,
                    provider=self.provider,
                    cloud_service_group=self.cloud_service_group,
                    cloud_service_type=self.cloud_service_type,
                )

    @staticmethod
    def _get_global_cdn_service_domain_list(global_cdn_service_domain_list):
        global_cdn_service_domain_list_info = []

        for global_cdn_service_domain in global_cdn_service_domain_list:
            info = {
                'service_domain_type_code': global_cdn_service_domain.service_domain_type_code,
                'protocol_type_code': global_cdn_service_domain.protocol_type_code,
                'default_domain_name': global_cdn_service_domain.default_domain_name,
                'user_domain_name': global_cdn_service_domain.user_domain_name
            }

            global_cdn_service_domain_list_info.append(info)

        return global_cdn_service_domain_list_info

    @staticmethod
    def _get_global_cdn_rule(global_cdn_rule):
        rule_data = {
            'protocol_type_code': global_cdn_rule.protocol_type_code,
            'service_domain_type_code': global_cdn_rule.service_domain_type_code,
            'origin_url': global_cdn_rule.origin_url,
            'origin_path': global_cdn_rule.origin_path,
            'origin_http_port': global_cdn_rule.origin_http_port,
            'origin_https_port': global_cdn_rule.origin_https_port,
            'forward_host_header_type_code': global_cdn_rule.forward_host_header_type_code,
            'forward_host_header': global_cdn_rule.forward_host_header,
            'cache_key_host_name_type_code': global_cdn_rule.cache_key_host_name_type_code,
            'is_gzip_compression_use': global_cdn_rule.is_gzip_compression_use,
            'caching_option_type_code': global_cdn_rule.caching_option_type_code,
            'is_error_contents_response_use': global_cdn_rule.is_error_contents_response_use,
            'caching_ttl_time': global_cdn_rule.caching_ttl_time,
            'is_query_string_ignore_use': global_cdn_rule.is_query_string_ignore_use,
            'is_remove_vary_header_use': global_cdn_rule.is_remove_vary_header_use,
            'is_large_file_optimization_use': global_cdn_rule.is_large_file_optimization_use,
            'gzip_response_type_code': global_cdn_rule.gzip_response_type_code,
            'is_referrer_domain_use': global_cdn_rule.is_referrer_domain_use,
            'referrer_domain_list': global_cdn_rule.referrer_domain_list,
            'is_referrer_domain_restrict_use': global_cdn_rule.is_referrer_domain_restrict_use,
            'is_secure_token_use': global_cdn_rule.is_secure_token_use,
            'secure_token_password': global_cdn_rule.secure_token_password,
            'is_reissue_secure_token_password': global_cdn_rule.is_reissue_secure_token_password,
            'certificate_name': global_cdn_rule.certificate_name,
            'is_access_log_use': global_cdn_rule.is_access_log_use,
            'access_log_file_storage_container_name': global_cdn_rule.access_log_file_storage_container_name
        }

        return rule_data

import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from inventory.connector.content_delivery.cdn_plus_connector import CdnPlusConnector

_LOGGER = logging.getLogger("cloudforet")


class CdnPlusManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Content Delivery"
        self.cloud_service_type = "Cdn Plus"
        self.provider = "naver cloud"
        self.metadata_path = "metadata/spaceone/content_delivery/cdn_plus.yaml"

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
        cdn_connector = CdnPlusConnector(secret_data=secret_data)
        cdn_instances = cdn_connector.list_cdn_plus_instance()

        for instance in cdn_instances:
            instance_name = instance.service_name
            instance_rule = instance.cdn_plus_rule
            instance_service_domain_list = instance.cdn_plus_service_domain_list
            cdn_plus_rule = self._get_cdn_plus_rule(instance_rule)
            cdn_plus_service_domain_list = self._get_cdn_plus_service_domain(instance_service_domain_list)

            instance_data = {
                'create_date': instance.create_date,
                'cdn_instance_status': instance.cdn_instance_status.code_name,
                'cdn_instance_operation': instance.cdn_instance_operation.code_name,
                'cdn_instance_status_name': instance.cdn_instance_status_name,
                'last_modified_date': instance.last_modified_date,
                'service_name': instance.service_name,
                'is_for_live_transcoder': instance.is_for_live_transcoder,
                'is_for_image_optimizer': instance.is_for_image_optimizer,
                'is_available_partial_domain_purge': instance.is_available_partial_domain_purge,
                'cdn_plus_service_domain_list': cdn_plus_service_domain_list,
                'cdn_plus_rule': cdn_plus_rule,
            }

            cloud_service = make_cloud_service(
                name=instance_name,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=instance_data,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )

    @staticmethod
    def _get_cdn_plus_rule(instance):
        rule_data = {
                'protocol_type_code': instance.protocol_type_code,
                'service_domain_type_code': instance.service_domain_type_code,
                'origin_url': instance.origin_url,
                'origin_http_port': instance.origin_http_port,
                'origin_https_port': instance.origin_https_port,
                'forward_host_header_type_code': instance.forward_host_header_type_code,
                'cache_key_host_name_type_code': instance.cache_key_host_name_type_code,
                'caching_option_type_code': instance.caching_option_type_code,
                'caching_ttl_time': instance.caching_ttl_time,
                'gzip_response_type_code': instance.gzip_response_type_code,
                'is_access_log_use': instance.is_access_log_use,
                'is_error_contents_response_use': instance.is_error_contents_response_use,
                'is_gzip_compression_use': instance.is_gzip_compression_use,
                'is_large_file_optimization_use': instance.is_large_file_optimization_use,
                'is_query_string_ignore_use': instance.is_query_string_ignore_use,
                'is_referrer_domain_restrict_use': instance.is_referrer_domain_restrict_use,
                'is_referrer_domain_use': instance.is_referrer_domain_use,
                'is_reissue_secure_token_password': instance.is_reissue_secure_token_password,
            }

        return rule_data

    @staticmethod
    def _get_cdn_plus_service_domain(service_list):
        cdn_plus_service_list = []
        for service in service_list:
            service_data = {
                'domain_id': service.domain_id,
                'service_domain_type_code': service.service_domain_type_code,
                'protocol_type_code': service.protocol_type_code,
                'default_domain_name': service.default_domain_name,
                'user_domain_name': service.user_domain_name,
            }
            cdn_plus_service_list.append(service_data)

        return cdn_plus_service_list

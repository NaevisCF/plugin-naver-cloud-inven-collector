from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
import importlib
import logging
from typing import List
import abc

_LOGGER = logging.getLogger(__name__)

CLOUD_SERVICE_MANAGER_MAP = {
    'VServer': 'ServerManager',
    'Server': 'VServerManager',
    'LoadBalancer': 'LoadBalancerManager',
    'Autoscaling': 'AutoscalingManager',
    'CdnPlus': 'CdnPlusManager',
    'CdnGlobal': 'CdnGlobalManager',
    # 'CloudDB': 'CloudDBManager',
    'VPC': 'VpcManager',
}


class ResourceManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.provider = "naver cloud"
        self.cloud_service_group = ""
        self.cloud_service_type = ""
        self.execute_managers = []

    def collect(self, options, secret_data, service):
        manager_instance = self._get_manager_instance(CLOUD_SERVICE_MANAGER_MAP[service])
        return manager_instance.collect_resources(options, secret_data)

    def collect_resources(self, options, secret_data):
        try:
            yield from self.collect_cloud_service_type(options, secret_data)
            yield from self.collect_cloud_service(options, secret_data)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type
            )

    def collect_cloud_service_type(self):
        cloud_service_types = self.create_cloud_service_type()
        for cloud_service_type in cloud_service_types:
            yield make_response(
                cloud_service_type=cloud_service_type,
                match_keys=[["name", "group", "provider"]],
                resource_type="inventory.CloudServiceType"
            )

    def collect_cloud_service(self, option: dict, secret_data: dict) -> List[dict]:
        cloud_services = self.create_cloud_service(option, secret_data)
        for cloud_service in cloud_services:
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[[
                    "reference.resource_id",
                    "provider",
                    "cloud_service_type",
                    "cloud_service_group",
                    "account",
                ]],
                resource_type="inventory.CloudService"
            )

    @staticmethod
    def get_service_names():
        service_names = []
        for service in CLOUD_SERVICE_MANAGER_MAP:
            service_names.append(service)
        return service_names

    @staticmethod
    def _get_manager_instance(name_or_object: [str, object], **kwargs):
        if isinstance(name_or_object, str):
            manager_module = importlib.import_module("inventory.manager")
            return getattr(manager_module, name_or_object)(**kwargs)

    @staticmethod
    def get_reference(resource_id: str, link: str) -> dict:
        return {
            "resource_id": resource_id,
            "external_link": link
        }

    @abc.abstractmethod
    def create_cloud_service_type(self):
        raise NotImplementedError(
            "method `create_cloud_service_type` should be implemented"
        )

    @abc.abstractmethod
    def create_cloud_service(self, region, options, secret_data, schema):
        raise NotImplementedError("method `create_cloud_service` should be implemented")

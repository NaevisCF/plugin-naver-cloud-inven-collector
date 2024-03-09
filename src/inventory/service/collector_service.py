import importlib
import logging

_LOGGER = logging.getLogger(__name__)

CLOUD_SERVICE_MANAGER_MAP = {
    'Server': 'ServerManager',
    'VServer': 'VServerManager',
    'LoadBalancer': 'LoadBalancerManager',
    'Autoscaling': 'AutoscalingManager',
    'CdnPlus': 'CdnPlusManager',
    'CdnGlobal': 'CdnGlobalManager',
    # 'CloudDB': 'CloudDBManager',
    'VPC': 'VpcManager',
}


class CollectorService:
    def __init__(self):
        self.execute_managers = []

    def collect(self, options, secret_data, service):

        manager_instance = self._get_manager_instance(CLOUD_SERVICE_MANAGER_MAP[service])
        return manager_instance.collect_resources(options, secret_data)

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

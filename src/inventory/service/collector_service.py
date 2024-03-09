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
    'CloudDB': 'CloudDBManager',
    'Vpc_Server': 'VpcServerManager',
    'Vpc': 'VpcManager',
    'Vpc_Autoscaling': 'VpcAutoscalingManager',
    'Vpc_LoadBalancer': 'VpcLoadBalancerManager',
    'ObjectStorage': 'ObjectStorageManager',
    'ArchiveStorage': 'ArchiveStorageManager'
}


class CollectorService:
    def __init__(self):
        self.execute_managers = []

    def collect(self, params):
        options = params.get("options", {})
        secret_data = params.get("secret_data", {})

        resource_type = options.get("resource_type")

        if resource_type == "inventory.CloudService":
            service = options.get("service")
            manager_instance = self._get_manager_instance(CLOUD_SERVICE_MANAGER_MAP[service])
            return manager_instance.collect_resources(options, secret_data)

        else:
            raise ValueError("Invalid resource type!")

    @staticmethod
    def _get_manager_instance(name_or_object: [str, object], **kwargs):
        if isinstance(name_or_object, str):
            manager_module = importlib.import_module("inventory.manager")
            return getattr(manager_module, name_or_object)(**kwargs)

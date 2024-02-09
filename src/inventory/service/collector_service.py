import importlib
import logging

_LOGGER = logging.getLogger(__name__)


class CollectorService:
    def __init__(self):
        self.execute_managers = []

    def collect(self, params):
        options = params.get("options", {})
        secret_data = params.get("secret_data", {})
        cloud_service_types = options.get("cloud_service_types", [])

        for execute_manager in cloud_service_types:
            manager_instance = self._get_manager_instance(execute_manager)
            return manager_instance.collect_resources(options, secret_data)

    @staticmethod
    def _get_manager_instance(name_or_object: [str, object], **kwargs):
        if isinstance(name_or_object, str):
            manager_module = importlib.import_module("inventory.manager")
            return getattr(manager_module, name_or_object)(**kwargs)

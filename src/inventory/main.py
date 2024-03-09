from typing import Generator
from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer
from inventory.service.collector_service import CollectorService

app = CollectorPluginServer()


@app.route('Collector.init')
def collector_init(params: dict) -> dict:
    return _create_init_metadata()


@app.route('Collector.verify')
def collector_verify(params: dict) -> None:
    pass


@app.route('Collector.collect')
def collector_collect(params: dict) -> Generator[dict, None, None]:
    options = params.get("options", {})
    secret_data = params.get("secret_data", {})
    resource_type = options.get("resource_type")

    if resource_type == "inventory.CloudService":
        services = options.get("services")
        for service in services:
            results = CollectorService().collect(options, secret_data, service)
            for result in results:
                yield result


@app.route('Job.get_tasks')
def job_get_tasks(params: dict) -> dict:
    """ Get job tasks

    Args:
        params (JobGetTaskRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'domain_id': 'str'
        }

    Returns:
        TasksResponse: {
            'tasks': 'list'
        }

    """

    tasks = []
    options = params.get("options", {})
    services = _set_service_filter(options)

    tasks.extend(_add_cloud_service_tasks(services))

    return {"tasks": tasks}


def _set_service_filter(options):
    available_services = CollectorService.get_service_names()

    if service_filter := options.get("service_filter"):
        _validate_service_filter(service_filter, available_services)
        return service_filter
    else:
        return available_services


def _validate_service_filter(service_filter, available_services):
    if not isinstance(service_filter, list):
        raise ValueError(
            f"Services input is supposed to be a list type! Your input is {service_filter}."
        )
    for each_service in service_filter:
        if each_service not in available_services:
            raise ValueError("Not a valid service!")


def _add_cloud_service_tasks(services: list) -> list:
    return [
        _make_task_wrapper(
            resource_type="inventory.CloudService", services=services
        )
    ]


def _make_task_wrapper(**kwargs) -> dict:
    task_options = {"task_options": {}}
    for key, value in kwargs.items():
        task_options["task_options"][key] = value
    return task_options


def _create_init_metadata():
    return {
        "metadata": {
            "supported_resource_type": [
                "inventory.CloudService",
                "inventory.CloudServiceType",
                "inventory.ErrorResource",
            ],
            "options_schema": {},
        }
    }

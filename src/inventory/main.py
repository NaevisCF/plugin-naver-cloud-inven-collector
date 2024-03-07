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
    service = CollectorService()
    return service.collect(params)


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
    services = ['VServer']
    options = params.get('options', {})

    tasks.extend(_add_cloud_service_type_tasks(services))

    return {"tasks": tasks}


def _add_cloud_service_type_tasks(services: list) -> list:
    return [
        _make_task_wrapper(
            resource_type="inventory.CloudServiceType", services=services
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
                "inventory.Region",
                "inventory.ErrorResource",
            ],
            "options_schema": {},
        }
    }

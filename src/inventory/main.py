from typing import Generator
from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer
from inventory.manager.compute.server_manager import ServerManager
from inventory.service.collector_service import CollectorService

app = CollectorPluginServer()


@app.route('Collector.init')
def collector_init(params: dict) -> dict:

    return {"metadata": { "options_schema": {}}}


@app.route('Collector.verify')
def collector_verify(params: dict) -> None:

    pass


@app.route('Collector.collect')
def collector_collect(params: dict) -> Generator[dict, None, None]:

    # options = params["options"]
    # secret_data = params["secret_data"]
    # schema = params.get("schema")
    #
    # server_mgr = ServerManager()
    # return server_mgr.collect_resources(options, secret_data)

    service = CollectorService()
    return service.collect(params=params)


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
    pass

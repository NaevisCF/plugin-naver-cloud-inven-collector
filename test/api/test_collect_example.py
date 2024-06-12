import os
import logging

from google.protobuf.json_format import MessageToDict
from spaceone.core import utils
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)


class TestCollectExample(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get("SPACEONE_TEST_CONFIG_FILE", "./config.yml")
    )
    global_config = config.get("GLOBAL", {})
    endpoints = global_config.get("ENDPOINTS", {})
    secrets = global_config.get("SECRETS", {})

    def test_init(self):
        v_info = self.inventory.Collector.init({"options": {}})
        print_json(v_info)

    def test_full_collect(self):
        secret_data = self.secrets

        print(f"Action 1: Generate Tasks!")
        print(f"=================== start get_tasks! ==========================")
        options = {
            "service_filter": None,
            "region_filter": None,
        }
        v_info = self.inventory.Job.get_tasks(
            {"options": options, "secret_data": secret_data}
        )
        print(f"=================== end get_tasks! ==========================")
        all_tasks = MessageToDict(v_info, preserving_proto_field_name=True)

        print(f"Action 2: Collect Resources!")
        print(
            f"=================== start collect_resources! =========================="
        )
        for task in all_tasks.get("tasks", []):
            task_options = task["task_options"]
            filter = {}
            params = {
                "options": task_options,
                "secret_data": secret_data,
                "filter": filter,
                "task_options": task_options
            }
            res_stream = self.inventory.Collector.collect(params)
            for res in res_stream:
                print_json(res)
        print(f"=================== end collect_resources! ==========================")

    def test_get_tasks(self):
        print(f"=================== start get_tasks! ==========================")
        options = {

        }
        v_info = self.inventory.Job.get_tasks(
            {"options": options, "secret_data": self.secrets}
        )
        print_json(v_info)


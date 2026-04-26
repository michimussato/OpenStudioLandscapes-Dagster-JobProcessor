from typing import Union, Dict

import gazu
import requests
from dagster import ConfigurableResource, OpExecutionContext, AssetExecutionContext


# https://rl-declarative-scheduling-dbt-translator.dagster.dagster-docs.io/concepts/resources


class KitsuResource(ConfigurableResource):
    host: str
    user: str
    password: str

    def get_kitsu_task_dict(
            self,
            task_id: str,
            context: Union[AssetExecutionContext, OpExecutionContext],
    ) -> Dict:
        gazu.client.set_host(self.host)
        try:
            gazu.log_in(
                email=self.user,
                password=self.password
            )
            task_dict = gazu.task.get_task(task_id=task_id)
        except (
            requests.exceptions.ConnectionError,
            gazu.exception.RouteNotFoundException
        ) as e:
            task_dict = {
                'kitsu_task_dict': {
                    'error': str(e)
                }
            }
            context.log.error(e)
        return task_dict

    def get_task_url(self, task_dict: Dict) -> str:
        gazu.client.set_host(self.host)
        gazu.log_in(
            email=self.user,
            password=self.password
        )
        task_url = gazu.task.get_task_url(task=task_dict)
        return task_url

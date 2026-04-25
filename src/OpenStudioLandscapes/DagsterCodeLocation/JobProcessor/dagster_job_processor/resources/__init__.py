from typing import Union, Dict

import gazu
import requests
from dagster import ConfigurableResource, OpExecutionContext, AssetExecutionContext
from pydantic import Field


# Resources
class KitsuResourceBase(ConfigurableResource):
    def get_kitsu_task_dict(self, **kwargs) -> Dict:
        raise NotImplementedError()

    def get_task_url(self, **kwargs) -> Dict:
        raise NotImplementedError()


class KitsuResource(KitsuResourceBase):
    host: str = Field(
        description="Gazu API host name.",
        # Todo:
        #  - [ ] can we get this from DeadlineConfigModel?
        default="http://10.1.2.15:4545/api",
    )
    user: str = Field(
        description="Gazu API username.",
        default="admin@example.com",
    )
    password: str = Field(
        description="Gazu API password.",
        default="mysecretpassword",
    )

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

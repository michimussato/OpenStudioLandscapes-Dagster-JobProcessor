import os

from dagster import (
    Definitions,
    load_assets_from_modules,
)

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.assets import read_yaml
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.resources.kitsu_resource import KitsuResource
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.sensors.yaml_ingestion_sensor import yaml_ingestion_sensor

read_yaml_assets = load_assets_from_modules(
    modules=[read_yaml],
    # auto_materialize_policy=AutoMaterializePolicy.lazy().with_rules(
    #         AutoMaterializeRule.materialize_on_parent_updated(),
    # )
)


all_sensors = [
    yaml_ingestion_sensor,
]


resources = {
    "local": {
        "kitsu_resource": KitsuResource(
            host="http://10.1.2.15:4545/api",
            user="admin@example.com",
            password="mysecretpassword",
        ),
    },
}


deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")


defs = Definitions(
    assets=[
        *read_yaml_assets,
    ],
    resources=resources[deployment_name],
    sensors=all_sensors,
)

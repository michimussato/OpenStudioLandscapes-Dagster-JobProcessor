import os

from dagster import (
    Definitions,
    load_assets_from_modules,
    AutoMaterializePolicy,
    AutoMaterializeRule,
)

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.assets import read_yaml
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.resources import (
    KitsuResource,
)
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.sensors import (
    # submission_sensor,
    job_processor_auto_materialize_sensor,
    ingestion_sensor_yaml,
)

read_yaml_assets = load_assets_from_modules(
    modules=[read_yaml],
    auto_materialize_policy=AutoMaterializePolicy.lazy().with_rules(
            AutoMaterializeRule.materialize_on_parent_updated(),
    )
)


all_sensors = [
    # submission_sensor,
    ingestion_sensor_yaml,
    job_processor_auto_materialize_sensor,
]


resources = {
    "local": {
        "kitsu_resource": KitsuResource(),
    },
    # "staging": {
    #     "kitsu_resource": KitsuResource(),
    # },
    # "farm": {
    #     "kitsu_resource": KitsuResource(),
    # },
}


deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")


defs = Definitions(
    assets=[
        *read_yaml_assets,
    ],
    resources=resources[deployment_name],
    sensors=all_sensors,
)

from dagster import (
    AssetSelection,
    define_asset_job,
    AssetKey,
)

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_POSTPROCESSOR


# This job requires a cross-code-location sensor
# https://docs.dagster.io/guides/automate/asset-sensors#getting-started
archive_yaml_job = define_asset_job(
    name="archive_yaml_job",
    selection=AssetSelection.assets(
        AssetKey([*ASSET_HEADER_JOB_POSTPROCESSOR["key_prefix"], "archive_job_yaml"]),
    )
)

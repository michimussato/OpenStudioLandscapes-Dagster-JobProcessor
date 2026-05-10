from dagster import (
    AssetSelection,
    define_asset_job,
    AssetKey,
)

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_POSTPROCESSOR

ingest_yaml_job = define_asset_job(
    name="ingest_yaml_job",
    selection=AssetSelection.all(
        include_sources=False,
    ) - AssetSelection.assets(
        AssetKey([*ASSET_HEADER_JOB_POSTPROCESSOR["key_prefix"], "archive_job_yaml"]),
    )
)

import textwrap

from dagster import (
    multi_asset_sensor,
    AssetKey,
    RunRequest,
    SkipReason,
    DefaultSensorStatus,
)

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.jobs.archive_yaml_job import archive_yaml_job

from OpenStudioLandscapes.DagsterCodeLocation.ShotProcessor.jobs.exr_to_png import ASSET_HEADER as ASSET_HEADER_OIIO_PROCESSOR_EXR_TO_PNG
from OpenStudioLandscapes.DagsterCodeLocation.ShotProcessor.jobs.exr_with_custom_metadata import ASSET_HEADER as ASSET_HEADER_OIIO_PROCESSOR_EXR_WITH_CUSTOM_METADATA
from OpenStudioLandscapes.DagsterCodeLocation.ShotProcessor.jobs.handle_overlay import ASSET_HEADER as ASSET_HEADER_OIIO_PROCESSOR_HANDLE_OVERLAY
from OpenStudioLandscapes.DagsterCodeLocation.ShotProcessor.jobs.mov_to_kitsu import ASSET_HEADER as ASSET_HEADER_OIIO_PROCESSOR_MOV_TO_KITSU
from OpenStudioLandscapes.DagsterCodeLocation.ShotProcessor.jobs.png_to_mov import ASSET_HEADER as ASSET_HEADER_OIIO_PROCESSOR_PNG_TO_MOV
from OpenStudioLandscapes.DagsterCodeLocation.ShotProcessor.jobs.text_overlay import ASSET_HEADER as ASSET_HEADER_OIIO_PROCESSOR_TEXT_OVERLAY


@multi_asset_sensor(
    monitored_assets=[
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_EXR_TO_PNG["key_prefix"], "job"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_EXR_TO_PNG["key_prefix"], "job_id"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_EXR_WITH_CUSTOM_METADATA["key_prefix"], "job"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_EXR_WITH_CUSTOM_METADATA["key_prefix"], "job_id"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_HANDLE_OVERLAY["key_prefix"], "job"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_HANDLE_OVERLAY["key_prefix"], "job_id"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_MOV_TO_KITSU["key_prefix"], "job"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_MOV_TO_KITSU["key_prefix"], "job_id"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_PNG_TO_MOV["key_prefix"], "job"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_PNG_TO_MOV["key_prefix"], "job_id"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_TEXT_OVERLAY["key_prefix"], "job"]),
        AssetKey([*ASSET_HEADER_OIIO_PROCESSOR_TEXT_OVERLAY["key_prefix"], "job_id"]),
    ],
    job=archive_yaml_job,
    minimum_interval_seconds=15,
    default_status=DefaultSensorStatus.RUNNING,
    description=textwrap.dedent(
        """
        Archive the submitted job YAML file into the render
        output directory. Only run this job after **all**
        upstream dependencies have been successfully materialized.
        
        For more information on `multi_asset_sensor`,
        see [Monitoring multiple assets](https://docs.dagster.io/guides/automate/asset-sensors#monitoring-multiple-assets).
        """
    ),
)
def archive_yaml_sensor(
    context
):
    asset_events = context.latest_materialization_records_by_key()
    if all(asset_events.values()):
        context.advance_all_cursors()
        return RunRequest(
            run_key=context.cursor,
            run_config={},
        )
    return None

import datetime

from dagster import (
    RunRequest,
    AssetKey,
    SensorResult,
    sensor,
    SensorEvaluationContext,
    DefaultSensorStatus,
)

import os
import pathlib
import shutil

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.config.models import DefaultConstants
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_PROCESSOR_READER

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.jobs.materialize_render_job import ingest_yaml_job


CONFIG: DefaultConstants = DefaultConstants()


# Todo:
#  - [ ] sensor vs asset_sensor
@sensor(
    job=ingest_yaml_job,
    default_status=DefaultSensorStatus.RUNNING,
    minimum_interval_seconds=15,
)
def yaml_ingestion_sensor(
        context: SensorEvaluationContext,
):
    path_to_submission_files = pathlib.Path(CONFIG.INPUT_ROOT)

    runs_to_request = []

    moves = []

    ext_yaml = [
        ".yml",
        ".yaml",
    ]

    for job_yaml in path_to_submission_files.glob('*.*'):

        if job_yaml.suffix in ext_yaml:

            context.log.info(f'Checking {job_yaml}...')

            context.log.info(f'Submission file is new: {job_yaml}...')

            CONFIG.INPUT_ROOT_PROCESSED.mkdir(mode=0o777, exist_ok=True, parents=True)
            output_file = CONFIG.INPUT_ROOT_PROCESSED / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}_{job_yaml.name}'
            # shutil.move(job_py, output_file)

            context.log.info(f'{output_file = }...')
            # context.log.info(f'{constants.INPUT_ROOT_PROCESSED = }...')
            context.log.info(f'{job_yaml = }...')

            runs_to_request.append(RunRequest(
                # whether or not a run will skip is based on the run_key that was assigned to previous ones
                run_key=f"ingested_jobs__{datetime.datetime.timestamp(datetime.datetime.now())}__{str(job_yaml).replace(os.sep, '__')}",
                run_config={
                    "ops": {
                        AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"]).to_python_identifier(): {
                            "config": {
                                "filename": str(output_file),
                                }
                            }
                        }
                    }
                )
            )

            moves.append({'src': job_yaml, 'dst': output_file})

    for i in moves:
        shutil.move(i['src'], i['dst'])

    return SensorResult(
        run_requests=runs_to_request,
    )

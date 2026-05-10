import datetime
import textwrap

from dagster import (
    RunRequest,
    AssetKey,
    SensorResult,
    sensor,
    SensorEvaluationContext,
    DefaultSensorStatus,
    SkipReason,
)

import os
import pathlib
import shutil

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.config.models import DefaultConstants
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.assets.read_yaml import ASSET_HEADER_JOB_PROCESSOR_READER

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.jobs.materialize_render_job import ingest_yaml_job


CONFIG: DefaultConstants = DefaultConstants()


# Todo:
#  - [ ] sensor vs asset_sensor?
#  - [ ] return None vs return SkipReason?
@sensor(
    job=ingest_yaml_job,
    default_status=DefaultSensorStatus.RUNNING,
    minimum_interval_seconds=15,
    description=textwrap.dedent(
        """
        Initiate a job to materialize all pre-processor assets
        and send jobs based on their results to the farm (ShotProcessor).
        Once all jobs are sent to the farm, a cleanup job will initiate
        some house-keeping (`archive_yaml_job`).
        """
    ),
)
def yaml_ingestion_sensor(
        context: SensorEvaluationContext,
):
    path_to_submission_files = pathlib.Path(CONFIG.INPUT_ROOT)

    runs_to_request = []

    # moves = []

    ext_yaml = [
        ".yml",
        ".yaml",
    ]

    p = path_to_submission_files.glob('*.*')
    yaml_files = [x for x in p if x.is_file() and x.suffix in ext_yaml]

    queue = sorted(yaml_files, key=os.path.getmtime)
    context.log.info(f"{queue = }")

    contents_processing = CONFIG.INPUT_ROOT_PROCESSING.iterdir()

    if any(contents_processing):
        context.log.warning(f"A file is still being processed: {list(contents_processing)}")
        # if there is a file in the .processing dir, don't
        # continue. Do one by one.
        # sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        return SkipReason(f"A file is still being processed: {list(contents_processing)}")

    # for job_yaml in path_to_submission_files.glob('*.*'):
    # for job_yaml in sorted(path_to_submission_files.iterdir(), key=os.path.getmtime):
    # fifo
    if not queue:
        context.log.info("Nothing to process; queue is empty.")
        return SkipReason("Nothing to process; queue is empty.")

    # while queue:
    next_ = queue.pop(0)
    # context.log.info(f"Processing {next_}...")
        # if next_.suffix in ext_yaml:
        #     break

    # for job_yaml in sorted(path_to_submission_files.glob("*.*"), key=os.path.getmtime):

        # if job_yaml.suffix in ext_yaml:

    context.log.info(f'Checking {next_}...')

    context.log.info(f'Submission file is new: {next_}...')

    # CONFIG.INPUT_ROOT_PROCESSED.mkdir(mode=0o777, exist_ok=True, parents=True)
    output_file = CONFIG.INPUT_ROOT_PROCESSING / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}_{next_.name}'
    # shutil.move(job_py, output_file)

    context.log.info(f'{output_file = }...')
    # context.log.info(f'{constants.INPUT_ROOT_PROCESSED = }...')
    context.log.info(f'{next_ = }...')

    runs_to_request.append(RunRequest(
        # whether or not a run will skip is based on the run_key that was assigned to previous ones
        run_key=f"ingested_jobs__{datetime.datetime.timestamp(datetime.datetime.now())}__{str(next_).replace(os.sep, '__')}",
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

    # moves.append({'src': next_, 'dst': output_file})

    # for i in moves:
    shutil.move(next_, output_file)

    return SensorResult(
        run_requests=runs_to_request,
    )

import enum
import pathlib
import re
import shutil

import requests
from typing import Any, Generator, Dict

import yaml
from dagster import (
    asset, AssetIn, MetadataValue,
    AssetMaterialization, Output,
    Config, AssetExecutionContext,
    AssetKey, multi_asset, AssetOut,
    RetryPolicy, Backoff, Jitter,
)
import json

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.config.models import DefaultConstants
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.dagster_job_processor.resources.kitsu_resource import KitsuResource
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.jobs.job_base import JobBase, Resolution
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.jobs import models_submission


# TODO
#  - [ ] rename to generate_job_submission_scripts
#  - [x] multi_asset for
#        - render_output_directory
#        - ~~render_output_filename~~ -> is a Dict
#        - render_version_directory
#        - version
#  - [x] multi_asset for
#        - ~~job_title~~
#        - job_title_str
#        - batch_name
#  - [x] multi_asset for
#        - frame_start
#        - frame_end
#        - frame_range
#  [...]


GROUP_JOB_PROCESSOR_READER = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_Reader"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR_READER = [GROUP_JOB_PROCESSOR_READER]

ASSET_HEADER_JOB_PROCESSOR_READER = {
    "group_name": GROUP_JOB_PROCESSOR_READER,
    "key_prefix": KEY_JOB_PROCESSOR_READER,
}


# Todo
#  - [ ] Rename to _PREPROCESSOR
GROUP_JOB_PROCESSOR = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_PreProcessor"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR = [GROUP_JOB_PROCESSOR]

ASSET_HEADER_JOB_PROCESSOR = {
    "group_name": GROUP_JOB_PROCESSOR,
    "key_prefix": KEY_JOB_PROCESSOR,
}


GROUP_JOB_PROCESSOR_PREPROCESSOR_KITSU = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_Kitsu"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR_PREPROCESSOR_KITSU = [GROUP_JOB_PROCESSOR_PREPROCESSOR_KITSU]

ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU = {
    "group_name": GROUP_JOB_PROCESSOR_PREPROCESSOR_KITSU,
    "key_prefix": KEY_JOB_PROCESSOR_PREPROCESSOR_KITSU,
}


GROUP_JOB_PROCESSOR_DEADLINE = "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_Deadline"
# KEY_CONSTANTS_DEFAULT = [GROUP_CONSTANTS_DEFAULT, "Constants"]
KEY_JOB_PROCESSOR_DEADLINE = [GROUP_JOB_PROCESSOR_DEADLINE]

ASSET_HEADER_JOB_PROCESSOR_DEADLINE = {
    "group_name": GROUP_JOB_PROCESSOR_DEADLINE,
    "key_prefix": KEY_JOB_PROCESSOR_DEADLINE,
}


class KitsuEntityTypes(enum.StrEnum):
    SHOT = "Shot"


def get_task_name(
        kitsu_dict: Dict,
) -> str:
    """
    {
      "task_type": {
        "allow_timelog": true,
        "archived": false,
        "color": "#F06292",
        "created_at": "2026-01-13T02:07:58",
        "department_id": "9cf1aa43-06f5-4e9a-a51a-2b1fd3ed3c2f",
        "description": null,
        "for_entity": "Shot",
        "id": "859d37ac-24e1-4fba-91a9-5c0479a11766",
        "name": "Rendering",
        "priority": 6,
        "short_name": "",
        "shotgun_id": null,
        "type": "TaskType",
        "updated_at": "2026-01-13T02:07:58"
      },
    }
    """
    _task_name = (
        kitsu_dict
        .get("task_type", {})
        .get("name", "No Task Name")
    )
    return _task_name


def get_entity_type(
        kitsu_dict: Dict,
) -> str:
    """
    {
      "entity_type": {
        "archived": false,
        "created_at": "2026-01-13T02:07:57",
        "description": null,
        "id": "6b85fb0f-a152-412e-b828-0a2c030b1393",
        "name": "Shot",
        "short_name": null,
        "type": "EntityType",
        "updated_at": "2026-01-13T02:07:57"
      },
    }
    """
    _entity_type = (
        kitsu_dict
        .get("entity_type", {})
        .get("name", "No Entity Type")
    )
    return _entity_type


def get_entity_name(
        kitsu_dict: Dict,
) -> str:
    """
    {
      "entity": {
        "canceled": false,
        "code": null,
        "created_at": "2026-03-14T22:38:44",
        "created_by": "108d7c11-b47b-4c4b-9fa2-f955e095d1b8",
        "data": {
          "fps": 25,
          "frame_in": 1201,
          "frame_out": 1250,
          "max_retakes": null,
          "resolution": "960x540"
        },
        "description": null,
        "entity_type_id": "6b85fb0f-a152-412e-b828-0a2c030b1393",
        "id": "89bcad46-1be7-4095-a5db-edeac55c04ab",
        "is_casting_standby": false,
        "is_shared": false,
        "name": "SH030",
        "nb_entities_out": 0,
        "nb_frames": 50,
        "parent_id": "dc80cc66-b934-4fe8-8bb3-cc90bf0a2348",
        "preview_file_id": "a8bad4a4-3d67-4350-8755-bf7976c80831",
        "project_id": "3ede4117-b73c-4bd3-83a2-40d66bc954c5",
        "ready_for": null,
        "shotgun_id": null,
        "source_id": null,
        "status": "running",
        "type": "Entity",
        "updated_at": "2026-03-23T09:43:42"
      },
    }
    """
    _entity_info = (
        kitsu_dict
        .get("entity", {})
        .get("name", "No Entity Name")
    )
    return _entity_info


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={},
    deps=[
        AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"]),
    ],
)
def CONFIG(
    context: AssetExecutionContext,
) -> Generator[
    Output[DefaultConstants] | AssetMaterialization,
    None,
    None,
]:

    config: DefaultConstants = DefaultConstants()

    context.log.debug(f"{config = }")

    yield Output(config)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(config.model_dump_json(fallback=str, indent=2)))}\n```"
            ),
        },
    )


class IngestJobConfig(Config):
    filename: str


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_READER,
    description="Parses the job file.",
)
def read_job_yaml(
        context: AssetExecutionContext,
        config: IngestJobConfig,
) -> Generator[Output[JobBase] | AssetMaterialization | Any, Any, None]:

    with open(config.filename) as fr:
        job_dict = yaml.safe_load(fr)

    context.log.debug(f"{job_dict = }")
    context.log.debug(f"{config.filename = }")

    job_model: JobBase = JobBase(
        **job_dict,
        job_file_yaml=pathlib.Path(config.filename),
    )

    context.log.debug(f"{job_model = }")

    yield Output(job_model)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(job_model.model_dump_json(fallback=str, indent=2)))}\n```"
            ),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU,
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    },
    retry_policy=RetryPolicy(
        max_retries=3,
        delay=0.2,  # 200ms
        backoff=Backoff.EXPONENTIAL,
        jitter=Jitter.PLUS_MINUS,
    ),
)
def get_kitsu_task_dict(
        context: AssetExecutionContext,
        kitsu_resource: KitsuResource,
        job_model: JobBase,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:
    """Returns a Kitsu task dict as a MaterializeResult object in the JSON format."""

    # TODO: make fail safe

    task_id = job_model.kitsu_task
    task_dict = kitsu_resource.get_kitsu_task_dict(
        context=context,
        task_id=str(task_id),
    )

    yield Output(task_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(task_dict),
        }
    )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR,
#     ins={
#         "get_kitsu_task_dict": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
#         )
#     },
# )
# def get_task_url(
#         context: AssetExecutionContext,
#         kitsu_resource: KitsuResource,
#         get_kitsu_task_dict: Dict,
# ) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
#     """Returns a Kitsu task dict as a MaterializeResult object in the JSON format."""
#     """
#     dagster._core.errors.DagsterExecutionStepExecutionError: Error occurred while executing op "OpenStudioLandscapes_DagsterCodeLocation_JobProcessor_PreProcessor__get_task_url":
#
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_plan.py", line 245, in dagster_event_sequence_for_step
#         yield from check.generator(step_events)
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_step.py", line 501, in core_dagster_event_sequence_for_step
#         for user_event in _step_output_error_checked_user_event_sequence(
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_step.py", line 184, in _step_output_error_checked_user_event_sequence
#         for user_event in user_event_sequence:
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/execute_step.py", line 88, in _process_asset_results_to_events
#         for user_event in user_event_sequence:
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/compute.py", line 190, in execute_core_compute
#         for step_output in _yield_compute_results(step_context, inputs, compute_fn, compute_context):
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/compute.py", line 159, in _yield_compute_results
#         for event in iterate_with_context(
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_utils/__init__.py", line 478, in iterate_with_context
#         with context_fn():
#       File "/opt/python3.11/lib/python3.11/contextlib.py", line 158, in __exit__
#         self.gen.throw(typ, value, traceback)
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/utils.py", line 86, in op_execution_error_boundary
#         raise error_cls(
#
#     The above exception was caused by the following exception:
#     KeyError: 'project_id'
#
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/utils.py", line 56, in op_execution_error_boundary
#         yield
#       File "/opt/python3.11/lib/python3.11/site-packages/dagster/_utils/__init__.py", line 480, in iterate_with_context
#         next_output = next(iterator)
#                       ^^^^^^^^^^^^^^
#       File "/opt/python3.11/lib/python3.11/site-packages/OpenStudioLandscapes/DagsterCodeLocation/JobProcessor/dagster_job_processor/assets/read_yaml.py", line 306, in get_task_url
#         task_url = kitsu_resource.get_task_url(task_dict=task_dict)
#                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#       File "/opt/python3.11/lib/python3.11/site-packages/OpenStudioLandscapes/DagsterCodeLocation/JobProcessor/dagster_job_processor/resources/kitsu_resource.py", line 46, in get_task_url
#         task_url = gazu.task.get_task_url(task=task_dict)
#                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#       File "/opt/python3.11/lib/python3.11/site-packages/gazu/cache.py", line 212, in wrapper
#         return function(*args, **kwargs)
#                ^^^^^^^^^^^^^^^^^^^^^^^^^
#       File "/opt/python3.11/lib/python3.11/site-packages/gazu/task.py", line 1575, in get_task_url
#         return f"{host}/productions/{task['project_id']}/shots/tasks/{task['id']}/"
#                                      ~~~~^^^^^^^^^^^^^^
#     """
#
#     # TODO: make fail safe
#
#     if "error" in get_kitsu_task_dict:
#         raise Exception(f"Kitsu task ID is set but can't get Task URL from Kitsu for this shot:\n"
#                         f"{get_kitsu_task_dict['error']}")
#
#     task_dict = get_kitsu_task_dict
#     task_url = kitsu_resource.get_task_url(task_dict=task_dict)
#
#     yield Output(task_url)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.url(task_url),
#         }
#     )


@multi_asset(
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "show_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "show_name"]),
        ),
        "task_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "task_name"]),
        ),
    },
    outs={
        "render_version_directory": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=pathlib.Path,
            description="The render base directory "
                        "where the version increments will be "
                        "created.",
        ),
        "version": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=str,
            description="The render base directory "
                        "where the version increments will be "
                        "created.",
        ),
        "render_output_directory": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=pathlib.Path,
            description="The full directory of a version "
                        "based on the `render_version_directory`.",
        ),
    },
)
def calc_render_output_directory(
        context: AssetExecutionContext,
        job_model: JobBase,
        get_kitsu_task_dict: Dict,
        show_name: str,
        task_name: str,
        CONFIG: DefaultConstants,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    ############################
    # render_version_directory #
    ############################

    # TODO: make this fail safe
    entity_name = get_entity_name(get_kitsu_task_dict)

    entity_type = get_entity_type(get_kitsu_task_dict)

    render_version_directory = CONFIG.OUTPUT_ROOT.joinpath(
        show_name,
        entity_type,
        entity_name,
        task_name,
    )
    render_version_directory.mkdir(parents=True, exist_ok=True)

    output_name = "render_version_directory"

    yield Output(
        output_name=output_name,
        value=render_version_directory,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ):  MetadataValue.path(render_version_directory),
        },
    )

    ###########
    # version #
    ###########

    # This directory must exist in order for it to be iterable

    pattern = re.compile(f"^[0-9]{{{CONFIG.PADDING_VERSION}}}")

    dirs = [i.name for i in render_version_directory.iterdir() if i.is_dir() and pattern.match(i.name)]
    dirs.append(str(0).zfill(CONFIG.PADDING_VERSION))
    dirs.sort()
    version_ = max(dirs)
    new_version = str(int(version_) + 1).zfill(CONFIG.PADDING_VERSION)
    new_version_dir = render_version_directory.joinpath(new_version)
    new_version_dir.mkdir(parents=True, exist_ok=True)

    output_name = "version"

    yield Output(
        output_name=output_name,
        value=new_version,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.text(new_version),
            "dirs": MetadataValue.json(dirs),
        },
    )

    ###########################
    # render_output_directory #
    ###########################

    render_output_directory = render_version_directory.joinpath(version)

    render_output_directory.mkdir(parents=True, exist_ok=True)

    kitsu_task_json = render_output_directory.joinpath("kitsu_task.json")

    if bool(job_model.kitsu_task):
        entity_type = get_entity_type(get_kitsu_task_dict)
        if entity_type == 'Shot':
            # filename = f'{str(handles)}_{str(job_model.cut_in - job_model.handles).zfill(CONFIG.PADDING)}-{str(job_model.cut_out + job_model.handles).zfill(CONFIG.PADDING)}_{str(handles)}'
            # with open(render_version_directory / filename, "w") as fw:
            #     fw.write(f"{str(job_model.kitsu_task) = }")
            # with open(render_version_directory / "kitsu_task_id.txt", "w") as fw:
            #     fw.write(str(job_model.kitsu_task))
            with open(kitsu_task_json, "w") as fw:
                json.dump(
                    get_kitsu_task_dict,
                    fw,
                    indent=2,
                    default=str,
                    ensure_ascii=True,
                    sort_keys=True,
                )

    output_name = "render_output_directory"

    yield Output(
        output_name=output_name,
        value=render_output_directory,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.path(render_output_directory),
            "kitsu_task_json": MetadataValue.path(kitsu_task_json),
        },
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "job_title": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title"])
        ),
        "output_format": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "output_format"])
        ),
        # "frame_start_absolute": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_start_absolute"])
        # ),
        # "frame_end_absolute": AssetIn(
        #     AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "frame_end_absolute"])
        # ),
    },
)
def render_output_filename(
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        job_model: JobBase,
        job_title: str,
        output_format: str,
        # frame_start_absolute: int,
        # frame_end_absolute: int,
) -> Generator[Output[Dict[str, str]] | AssetMaterialization | Any, Any, None]:

    # padding_bash_expansion = "{%i..%i}" % (frame_start_absolute, frame_end_absolute)
    padding_deadline = f"{job_model.plugin_model.padding_deadline}"
    padding_deadline_batch_startframe = f"{job_model.plugin_model.padding_deadline_batch_startframe}"
    padding_deadline_batch_endframe = f"{job_model.plugin_model.padding_deadline_batch_endframe}"
    padding_command = f"{job_model.plugin_model.padding_command}"
    padding_oiiotool = f"{job_model.plugin_model.padding_oiiotool}"

    # Don't uncomment
    # Required to eval(padding_deadline) and eval(padding_command)
    EVAL_PADDING = CONFIG.PADDING

    ret = {
        # "padding_bash_expansion": f"{job_title}.{padding_bash_expansion}.{output_format}",
        "padding_deadline": f"{job_title}.{eval(padding_deadline)}.{output_format}",
        "padding_deadline_batch_startframe": f"{job_title}.{eval(padding_deadline_batch_startframe)}.{output_format}",
        "padding_deadline_batch_endframe": f"{job_title}.{eval(padding_deadline_batch_endframe)}.{output_format}",
        "padding_command": f"{job_title}.{eval(padding_command)}.{output_format}",
        "padding_oiiotool": f"{job_title}.{eval(padding_oiiotool)}.{output_format}",
    }

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```json\n{json.dumps(ret, indent=2, default=str, sort_keys=True)}\n```"
            ),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def job_title(
        context: AssetExecutionContext,
        job_model: JobBase,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    """
    Create job title from the job_file:
    /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
    -> vivi_025
    """

    base, first_dot, rest = job_model.job_file.name.partition(".")

    yield Output(base)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(base),
            "job_file".join(context.asset_key.path): MetadataValue.path(job_model.job_file),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
    }
)
def show_name(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[str | Any] | AssetMaterialization | Any, Any, None]:

    ret = (
        get_kitsu_task_dict
        .get("project", {})
        .get("name", "No Show")
    )

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
    }
)
def task_name(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
) -> Generator[Output[str | Any] | AssetMaterialization | Any, Any, None]:

    ret = get_task_name(get_kitsu_task_dict)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(ret)
        }
    )


@multi_asset(
    ins={
        "version": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "version"]),
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "show_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "show_name"])
        ),
        "task_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "task_name"]),
        ),
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "cut_in": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "cut_in"])
        ),
        "cut_out": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "cut_out"])
        ),
    },
    outs={
        "job_title_str": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=str,
            description="Todo",
        ),
        "batch_name": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=str,
            description="Todo",
        ),
    },
)
def deadline_job_str(
        context: AssetExecutionContext,
        version: str,
        CONFIG: DefaultConstants,
        job_model: JobBase,
        show_name: str,
        task_name: str,
        get_kitsu_task_dict: Dict,
        cut_in: int,
        cut_out: int,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:

    entity_name = get_entity_name(get_kitsu_task_dict)
    entity_type = get_entity_type(get_kitsu_task_dict)

    if bool(job_model.kitsu_task):
        if entity_type == KitsuEntityTypes.SHOT.value:
            entity_name = f'{entity_name} - {str(job_model.handles)}_{str(cut_in).zfill(CONFIG.PADDING)}-{str(cut_out).zfill(CONFIG.PADDING)}_{job_model.handles}'
            # entity_name = f'{self.sequence_name}_{self.entity_name} - {str(self.handles)}_{str(self.frame_start).zfill(self.PADDING)}-{str(self.frame_end).zfill(self.PADDING)}_{self.handles}'

    job_title_str = f'{show_name} - {entity_name} - {task_name} - {job_model.job_file.name} - {version} - {pathlib.Path(job_model.plugin_model.executable).name}'

    #################
    # job_title_str #
    #################

    output_name = "job_title_str"

    yield Output(
        output_name=output_name,
        value=job_title_str,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.path(job_title_str),
        },
    )

    ##############
    # batch_name #
    ##############

    batch_name = f"Batch: {job_title_str}"

    output_name = "batch_name"

    yield Output(
        output_name=output_name,
        value=batch_name,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.path(batch_name),
        },
    )


@multi_asset(
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
    },
    outs={
        "cut_in": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=int,
            description="Cut range IN.",
        ),
        "cut_out": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=int,
            description="Cut range OUT.",
        ),
        "work_in": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=int,
            description="Work range IN: cut_in - Handles.",
        ),
        "work_out": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=int,
            description="Work range OUT: cut_out + Handles.",
        ),
        "render_frames": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR,
            dagster_type=str,
            description="Todo",
        ),
    },
)
def calc_frames(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        job_model: JobBase,
        CONFIG: DefaultConstants,
):

    """
    frame_in = get_kitsu_task_dict["entity"]["data"]["frame_in"]
    frame_out = get_kitsu_task_dict["entity"]["data"]["frame_out"]
    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]

    Priorities:
    1. [x] manual via config
    2. [x] Kitsu Shot
    3. [ ] Kitsu Project
    4. [x] Config Default
    """

    cut_in = job_model.cut_in \
            or get_kitsu_task_dict.get("entity", {}).get("data", {}).get("frame_in", 0) \
            or job_model.cut_in_default

    cut_out = job_model.cut_out \
            or get_kitsu_task_dict.get("entity", {}).get("data", {}).get("frame_out", 0) \
            or job_model.cut_out_default

    # extend work range with handles
    work_in = cut_in - job_model.handles
    work_out = cut_out + job_model.handles

    if any([i < 0 for i in [work_in, work_out]]):
        if CONFIG.DONT_ALLOW_NEGATIVE_FRAMES:
            raise Exception("Negative frames not allowed")

    ###########
    # work_in #
    ###########

    output_name = "work_in"

    yield Output(
        output_name=output_name,
        value=work_in,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.int(work_in),
        },
    )

    ############
    # work_out #
    ############

    output_name = "work_out"

    yield Output(
        output_name=output_name,
        value=work_out,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.int(work_out),
        },
    )

    ##########
    # cut_in #
    ##########

    output_name = "cut_in"

    yield Output(
        output_name=output_name,
        value=cut_in,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.int(cut_in),
        },
    )

    ###########
    # cut_out #
    ###########

    output_name = "cut_out"

    yield Output(
        output_name=output_name,
        value=cut_out,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.int(cut_out),
        },
    )

    #################
    # render_frames #
    #################

    # make sure we filter frame jumps according to the chunk_size
    # for nuke, render time could be way slower if it has
    # to be launched for every single frame
    # frame_jumps = [i for i in constants.FRAME_JUMPS if i <= combine_dicts["yaml_submission"]["chunk_size"]]

    if job_model.chunk_size > 1:
        frame_jumps = [min(CONFIG.FRAME_JUMPS)]
    else:
        frame_jumps = CONFIG.FRAME_JUMPS

    frame_list = ",".join([
        f"{work_in}-{work_out}x{int(i)}"
        for i in frame_jumps
    ])

    output_name = "render_frames"

    yield Output(
        output_name=output_name,
        value=frame_list,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(
                context.asset_key_for_output(output_name).path
            ): MetadataValue.text(frame_list),
        },
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "get_kitsu_task_dict": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def fps(
        context: AssetExecutionContext,
        get_kitsu_task_dict: Dict,
        job_model: JobBase,
) -> Generator[Output[float] | AssetMaterialization | Any, Any, None]:

    """
    frame_in = get_kitsu_task_dict["entity"]["data"]["frame_in"]
    frame_out = get_kitsu_task_dict["entity"]["data"]["frame_out"]
    nb_frames = get_kitsu_task_dict["entity"]["nb_frames"]

    Priorities:
    1. manual via config
    2. Kitsu Shot
    3. Kitsu Project
    4. Config Default
    """

    if bool(job_model.kitsu_task):
        if "error" in get_kitsu_task_dict:
            raise Exception(f"Kitsu task ID is set but can't get FPS from Kitsu for this shot:\n"
                            f"{get_kitsu_task_dict['error']}")

    # if bool(read_job_py["kitsu_task"]):
    fps_job = job_model.fps

    fps_kitsu_project = float(get_kitsu_task_dict.get("project", {}).get("fps", 0))

    kitsu_entity_type = get_entity_type(get_kitsu_task_dict)
    fps_kitsu_shot = float(0)
    if kitsu_entity_type == "Shot":
        fps_kitsu_entity = fps_kitsu_shot = float(get_kitsu_task_dict.get("entity", {}).get("data", {}).get("fps", 0))

    yield Output(fps_job)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.float(fps_job),
            "fps_job": MetadataValue.float(fps_job),
            "fps_kitsu_project": MetadataValue.float(fps_kitsu_project),
            "kitsu_entity_type": MetadataValue.text(kitsu_entity_type),
            "fps_kitsu_shot": MetadataValue.float(fps_kitsu_shot),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    },
    description="Returns the output format of the render."
)
def output_format(
        context: AssetExecutionContext,
        job_model: JobBase,
) -> Generator[Output[Any] | AssetMaterialization | Any, Any, None]:

    # if read_job_py["output_format"] is None:
    #     raise ValueError("output_format is not defined.")

    # if job_model.output_format not in read_job_py["plugin_dict"]["submitter"]["output_formats_plugin"]:
    #     raise ValueError(f"output_format is not supported: {read_job_py['output_format']}")

    yield Output(job_model.output_format)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.text(job_model.output_format)
        }
    )


@multi_asset(
    outs={
        "job_info_model": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
            dagster_type=models_submission.JobInfo,
            description="",
        ),
    },
    ins={
        "batch_name": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "batch_name"])
        ),
        "job_title_str": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "job_title_str"])
        ),
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "render_frames": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_frames"])
        ),
        "render_output_filename": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def job_info(
        context: AssetExecutionContext,
        batch_name: str,
        job_title_str: str,
        render_output_directory: pathlib.Path,
        render_frames: str,
        render_output_filename: Dict,
        job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#job-info-file-options
    # render_output_directory.mkdir(parents=True, exist_ok=True)
    path = render_output_directory / "jobinfo_info.txt"

    context.log.debug(f"{path = }")

    job_info_dict = {
        "Plugin": models_submission.DeadlinePlugins.CommandLine.value,
        "Frames": render_frames,
        "Name": job_title_str,
        "Comment": job_model.comment,
        # "Department"
        "BatchName": batch_name,
        "UserName": job_model.deadline_config.user,
        "MachineName": job_model.deadline_config.host,
        # "Pool"
        # "SecondaryPool"
        # "Group"
        "Priority": job_model.job_priority,
        "ChunkSize": job_model.chunk_size,
        # "ConcurrentTasks"
        # "LimitConcurrentTasksToNumberOfCpus"
        # "OnJobComplete"
        # "SynchronizeAllAuxiliaryFiles"
        "ForceReloadPlugin": True,
        # "Sequential"
        # "SuppressEvents"
        # "Protected"
        "InitialStatus": job_model.deadline_initial_status,
        # "StartupDirectory"
        "OutputDirectory0": render_output_directory.as_posix(),
        "OutputFilename0": render_output_filename["padding_deadline"],
    }

    job_info = models_submission.JobInfo(
        **job_info_dict,
    )

    context.log.debug(f"{job_info = }")

    output_name = "job_info_model"

    yield Output(
        output_name=output_name,
        value=job_info,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "job_info_model_yaml": MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(job_info.model_dump_json(indent=2, fallback=str)))}\n```"
            ),
        }
    )


@multi_asset(
    outs={
        "plugin_info_model": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
            dagster_type=models_submission.CommandLinePluginInfo,
            description="",
        ),
    },
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "render_arguments": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_arguments"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def plugin_info(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        render_arguments: str,
        job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    # render_output_directory.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(f"{render_output_directory}/plugin_info.txt")

    context.log.debug(f"{path = }")

    plugin_info_dict = {
        "Executable": job_model.plugin_model.executable.as_posix(),
        "Arguments": f"{render_arguments}",
    }

    plugin_info = models_submission.CommandLinePluginInfo(
        **plugin_info_dict,
    )

    context.log.debug(f"{plugin_info = }")

    output_name = "plugin_info_model"

    yield Output(
        output_name=output_name,
        value=plugin_info,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "plugin_info_model_yaml": MetadataValue.md(
                f"```yaml\n{yaml.safe_dump(json.loads(plugin_info.model_dump_json(indent=2, fallback=str)))}\n```"
            ),
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    }
)
def archive_job_yaml(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        job_model: JobBase,
) -> Generator[Output[pathlib.Path] | AssetMaterialization | Any, Any, None]:

    job_yaml = job_model.job_file_yaml

    if not render_output_directory.exists():
        raise FileNotFoundError(f"Rendering output directory {render_output_directory} does not exist yet.")

    try:
        shutil.move(job_yaml, render_output_directory)
    except FileNotFoundError as e:
        context.log.warning(f"Job YAML file {job_yaml} not found: {e}")

    ret = pathlib.Path(render_output_directory) / job_yaml.name

    if not ret.exists():
        raise FileNotFoundError(f"Job YAML file {job_yaml.name} could not be found in {render_output_directory}")

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(ret)
        }
    )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR,
    ins={
        "render_output_directory": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_directory"])
        ),
        "render_output_filename": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "render_output_filename"])
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"])
        ),
    }
)
def render_arguments(
        context: AssetExecutionContext,
        render_output_directory: pathlib.Path,
        render_output_filename: Dict,
        job_model: JobBase,
        CONFIG: DefaultConstants,
) -> Generator[Output[str] | AssetMaterialization | Any, Any, None]:
    args = job_model.plugin_model.args
    render_output = render_output_directory / CONFIG.RENDER_RAW_OUT / render_output_filename["padding_command"]

    job_model_dict = json.loads(
        job_model.model_dump_json(
            fallback=str,
        )
    )
    # Todo:
    #  - [x] why output_format had to be capital here?
    #        combine_dicts["yaml_submission"]["output_format"] = combine_dicts["yaml_submission"]["output_format"].upper()
    #        -> Blender requires that. Logic moved to the Blender Plugin
    job_model_dict["output_format"]: str = job_model_dict["output_format"].upper()

    plugin_model_dict = json.loads(
        job_model.plugin_model.model_dump_json(
            fallback=str,
        )
    )

    context.log.debug(f"{args = }")
    context.log.debug(f"{render_output = }")
    context.log.debug(f"{job_model_dict = }")
    context.log.debug(f"{plugin_model_dict = }")

    ret = " ".join(args).format(
        render_output=render_output.as_posix(),
        **job_model_dict,
        **plugin_model_dict,
    )

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(f"```\n{ret}\n```"),
        }
    )


# @asset(
#     **ASSET_HEADER_JOB_PROCESSOR,
#     ins={
#         "get_kitsu_task_dict": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_PREPROCESSOR_KITSU["key_prefix"], "get_kitsu_task_dict"])
#         ),
#         "job_model": AssetIn(
#             AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
#         ),
#     }
# )
# def resolution(
#         context: AssetExecutionContext,
#         get_kitsu_task_dict: Dict,
#         job_model: JobBase,
# ) -> Generator[Output[Resolution] | AssetMaterialization | Any, Any, None]:
#     """
#     Priorities:
#     1. manual via config
#     2. Kitsu Shot
#     3. Kitsu Project
#     4. Config Default
#     """
#
#     resolution_job: Resolution = job_model.resolution
#
#     resolution_kitsu_project = Resolution(*tuple(int(i) for i in str(get_kitsu_task_dict.get("project", {}).get("resolution", "0x0")).split("x")))
#     resolution_kitsu_shot = Resolution(*tuple(int(i) for i in str(get_kitsu_task_dict.get("entity", {}).get("data", {}).get("resolution", "0x0")).split("x")))
#
#     yield Output(resolution_job)
#
#     yield AssetMaterialization(
#         asset_key=context.asset_key,
#         metadata={
#             "__".join(context.asset_key.path): MetadataValue.json(resolution_job),
#             "resolution_job": MetadataValue.json(resolution_job),
#             "resolution_kitsu_project": MetadataValue.json(resolution_kitsu_project),
#             "resolution_kitsu_shot": MetadataValue.json(resolution_kitsu_shot),
#         }
#     )


@asset(
    **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "job_info_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "job_info_model"]),
        ),
        "plugin_info_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "plugin_info_model"]),
        ),
    },
)
def payload_raw(
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        job_info_model: models_submission.JobInfo,
        plugin_info_model: models_submission.CommandLinePluginInfo,
) -> Generator[Output[Dict] | AssetMaterialization | Any, Any, None]:

    """
    Before:
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/037/4_1197-1254_4/combined_dict.json"

    After
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/045/4_0997-1104_4/combined_dict.json"
    """

    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
    }

    context.log.debug(f"{headers = }")

    # https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/manual/rest-jobs.html#submit-job
    payload_raw = {
        "JobInfo": json.loads(job_info_model.model_dump_json(indent=2, fallback=str)),
        "PluginInfo": json.loads(plugin_info_model.model_dump_json(indent=2, fallback=str)),
        "IdOnly": False,
        "AuxFiles": [],
    }

    context.log.debug(f"{payload_raw = }")

    yield Output(payload_raw)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.md(
                f"```json\n{json.dumps(payload_raw, default=str, sort_keys=True, indent=CONFIG.JSON_INDENT)}\n```"
            ),
        }
    )


@multi_asset(
    outs={
        "job_raw": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
            dagster_type=Dict,
            description="",
        ),
        "job_id_raw": AssetOut(
            **ASSET_HEADER_JOB_PROCESSOR_DEADLINE,
            dagster_type=str,
            description="",
        ),
    },
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR["key_prefix"], "CONFIG"]),
        ),
        "payload_raw": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_DEADLINE["key_prefix"], "payload_raw"]),
        ),
        "job_model": AssetIn(
            AssetKey([*ASSET_HEADER_JOB_PROCESSOR_READER["key_prefix"], "read_job_yaml"])
        ),
    },
)
def submit_request_raw(
        context: AssetExecutionContext,
        CONFIG: DefaultConstants,
        payload_raw: Dict,
        job_model: JobBase,
) -> Generator[Output[requests.Response] | AssetMaterialization | Any, Any, None]:

    """
    Before:
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/037/4_1197-1254_4/combined_dict.json"

    After
    cat "/data/share/AWSPortalRoot1/out/Test Production/Shot/SH030/Rendering/045/4_0997-1104_4/combined_dict.json"
    """

    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
    }

    context.log.debug(f"{headers = }")

    payload = json.dumps(payload_raw, indent=CONFIG.JSON_INDENT, sort_keys=True, default=str)

    context.log.debug(f"{payload = }")

    context.log.info(f"Sending request to {job_model.deadline_config.rest_api_jobs}...")

    # Requests: data vs. json:
    # - https://stackoverflow.com/a/26685359/2207196
    # - https://requests.readthedocs.io/en/latest/user/quickstart/#more-complicated-post-requests
    #   > If you need that header set and you don’t want to encode the dict yourself, you can
    #   > also pass it directly using the json parameter (added in version 2.4.2) and it will
    #   > be encoded automatically
    # -> using `json=` does not serialize as expected (yet). Hence, `data=` and manual.
    request = requests.Request(
        url=job_model.deadline_config.rest_api_jobs,
        method="POST",
        headers=headers,
        # json=payload_raw,
        data=payload,
    )

    context.log.debug(f"{request = }")

    prepared_request = request.prepare()

    context.log.debug(f"{prepared_request = }")

    session = requests.Session()
    response = session.send(prepared_request, verify=False)

    context.log.debug(f"{response = }")
    context.log.debug(f"{response.raw = }")
    context.log.debug(f"{response.status_code = }")
    # context.log.debug(f"{response.content = }")
    context.log.debug(f"{response.text = }")

    output_name = "job_raw"

    yield Output(
        output_name=output_name,
        value=response.json(),
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(context.asset_key_for_output(output_name).path): MetadataValue.json(payload),
            "headers": MetadataValue.md(
                f"```json\n{json.dumps(headers, default=str, sort_keys=True, indent=CONFIG.JSON_INDENT)}\n```"
            ),
            "payload": MetadataValue.md(
                f"```json\n{payload}\n```"
            ),
            "request": MetadataValue.md(
                f"```json\n{json.dumps(request.__dict__, indent=CONFIG.JSON_INDENT, default=str, sort_keys=True)}\n```"
            ),
            "response": MetadataValue.md(
                f"```json\n{json.dumps(response.json(), default=str, sort_keys=True, indent=CONFIG.JSON_INDENT)}\n```"
            ),
        }
    )

    output_name = "job_id_raw"

    _id = response.json().get("_id", None)

    yield Output(
        output_name=output_name,
        value=_id,
    )

    yield AssetMaterialization(
        asset_key=context.asset_key_for_output(output_name),
        metadata={
            "__".join(context.asset_key_for_output(output_name).path): MetadataValue.path(_id),
        }
    )

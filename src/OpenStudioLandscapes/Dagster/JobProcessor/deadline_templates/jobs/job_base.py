import datetime
import uuid
import enum

class InitialStatuses(enum.StrEnum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"

class OutputFormats(enum.StrEnum):
    PNG = "png"
    EXR = "exr"
    JPG = "jpg"
    TGA = "tga"

job: dict = {
    "job_file": None,
    "plugin_dict": {},
    "plugin_file": None,
    "job_uuid": str(uuid.uuid4()),
    "job_timestamp": str(datetime.datetime.timestamp(datetime.datetime.now())),
    "handles": 4,
    "output_formats": [str(i.value) for i in OutputFormats],
    "output_format": OutputFormats.EXR.value,
    "chunk_size": 1,
    "initial_statuses": [str(i.value) for i in InitialStatuses],
    "deadline_initial_status": InitialStatuses.SUSPENDED.value,
    "append_draft_job_png": False,
    "append_draft_job_mov": False,
    "with_kitsu_publish": False,
    "deadline_job_with_draft": False,
    "comment": "",
    "frame_start": 1001,
    "frame_end": 1100,
    "resolution_draft_scale": 0.5,
    "kitsu_task": "",  # SQ010 / SQ010_SH030  Layout  http://miniboss/productions/6c5dfed4-0f11-48f7-aba2-4d4d5cce85fc/shots/tasks/9bb09bfa-0a97-40c6-a6e6-27405b198570
}

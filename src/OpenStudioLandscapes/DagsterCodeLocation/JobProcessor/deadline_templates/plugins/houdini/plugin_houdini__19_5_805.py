import pathlib
from typing import Literal

from pydantic.fields import Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.houdini import PluginHoudiniBase


class PluginHoudini_19_5_805(PluginHoudiniBase):
    plugin_type: Literal['PluginHoudini_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "hrender"

    # Farm command:
    # Executable=/nfs/rez-packages/wrappers/hython-19.5.805
    # Arguments="/nfs/deadline/DeadlineRepository10/plugins/Houdini/hrender_dl.py -e -f <STARTFRAME> <ENDFRAME> 1 -d /stage/usdrender_rop_camera2 -o <QUOTE>/nfs/AWSPortalRoot1/out/Sandbox/Shot/SQ010_SH020/Layout/018/4_0997-1024_4/vivi_025.\$F4.exr<QUOTE> <QUOTE>/nfs/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip<QUOTE>"

    rop: str = Field(
        default="",
        description="The path to the render operator (ROP) to use "
                    "for rendering.",
    )

import pathlib
from typing import Literal

from pydantic.fields import Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.houdini import (
    PluginHoudiniBase,
    PluginHoudiniKarmaBase,
)


class PluginHoudini_19_5_805(PluginHoudiniBase):
    plugin_type: Literal['PluginHoudini_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "hrender"

    # Farm command:
    # Executable=/nfs/rez-packages/wrappers/hython-19.5.805
    # Arguments="/nfs/deadline/DeadlineRepository10/plugins/Houdini/hrender_dl.py -e -f <STARTFRAME> <ENDFRAME> 1 -d /stage/usdrender_rop_camera2 -o <QUOTE>/nfs/AWSPortalRoot1/out/Sandbox/Shot/SQ010_SH020/Layout/018/4_0997-1024_4/vivi_025.\$F4.exr<QUOTE> <QUOTE>/nfs/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip<QUOTE>"
    # Arguments="/nfs/deadline/DeadlineRepository10/plugins/Houdini/hrender_dl.py -e -f <STARTFRAME> <ENDFRAME> 1 -d /stage/usdrender_rop_camera2 -o <QUOTE>/nfs/AWSPortalRoot1/out/Sandbox/Shot/SQ010_SH020/Layout/018/4_0997-1024_4/vivi_025.\$F4.exr<QUOTE> <QUOTE>/data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip<QUOTE>"

    # https://deborahrfowler.com/HoudiniResources/Overview-CommandLineRenderingMantraRedshift.html
    # /data/share/rez-packages/packages/houdini/19.5.805/hython /data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/plugins/Houdini/hrender_dl.py -e -f 1001 1001 1 -v -d "/stage/usdrender_rop_camera2" -o "/data/share/AWSPortalRoot1/test/vivi_025.$F4.exr" "/data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip"
    # /data/share/rez-packages/packages/houdini/19.5.805/hython /data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/plugins/Houdini/hrender_dl.py -e -f 1001 1002 1 -v -d "/stage/usdrender_rop_camera2" -o '/data/share/AWSPortalRoot1/test/vivi_025.\$F4.exr' '/data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip'
    # /data/share/rez-packages/packages/houdini/19.5.805/hython /data/local/.openstudiolandscapes/.landscapes/.persistent/OpenStudioLandscapes-Deadline-10-2/data/opt/Thinkbox/DeadlineRepository10/plugins/Houdini/hrender_dl.py -e -f 1001 1001 1 -v -d "/stage/usdrender_rop_camera2" -o '/data/share/AWSPortalRoot1/test/vivi_025.\$F4.exr' '/data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip'

    # /data/share/tools/houdini-19.5.805-linux_x86_64_gcc9.3# hrender -v -e -f 1001 1002 -i 1 -d /stage/usdrender_rop_camera2 /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip

    rop: str = Field(
        default="",
        description="The path to the render operator (ROP) to use "
                    "for rendering.",
    )


class PluginHoudiniKarma_19_5_805(PluginHoudiniKarmaBase):
    plugin_type: Literal['PluginHoudini_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "husk"

import pathlib
import textwrap
from typing import Literal

from pydantic import Field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import (
    houdini,
)


class PluginHoudini_19_5_805(houdini.PluginHoudiniHrenderBase):
    plugin_type: Literal['PluginHoudini_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "hrender"

    rop: str = Field(
        default="",
        description="The path to the render operator (ROP) to use "
                    "for rendering.",
    )

    help_command: str = textwrap.dedent(
        """
        ```shell
        cd /data/share/tools/houdini-19.5.805-linux_x86_64_gcc9.3
        . houdini_setup
        hrender
        ```
        """
    )

    farm_command: str = textwrap.dedent(
        """
        Todo:
         - [ ] Verify that this actually works
        
        ```shell
        hrender \
            -v \
            -e \
            -f 1002 1003 \
            -i 1 \
            -d /stage/usdrender_rop_camera2 \
            /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip
        ```
        """
    )


class PluginHoudiniKarma_19_5_805(houdini.PluginHoudiniKarmaBase):
    plugin_type: Literal['PluginHoudiniKarma_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "husk"

    help_command: str = textwrap.dedent(
        """
        ```shell
        /data/share/rez-packages/packages/houdini/19.5.805/husk --help
        ```
        """
    )

    farm_command: str = textwrap.dedent(
        """
        ```shell
        /data/share/rez-packages/packages/houdini/19.5.805/husk \
            --verbose ce9 \
            --settings /Render/rendersettings \
            --make-output-path \
            --frame 1021 \
            --frame-count 10 \
            --frame-inc 1 \
            --renderer BRAY_HdKarma \
            --purpose geometry,render \
            --complexity veryhigh \
            --snapshot 300 \
            --output \"/data/share/AWSPortalRoot1/out/Test Production/Shot/SH040/Rendering/002/raw/vivi_025.\\\$F4.exr\" \
            --usd-input \"/data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda\"
        ```
        """
    )

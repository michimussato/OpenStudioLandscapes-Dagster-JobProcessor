import pathlib
import textwrap
from typing import Literal

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.nuke import PluginNukeBase


class PluginNuke_15_1v1(PluginNukeBase):
    plugin_type: Literal['PluginNuke_15_1v1']

    executable: pathlib.Path = REZ_PACKAGES / "nuke" / "15.1v1" / "nuke"

    farm_command: str = textwrap.dedent(
        """
            /data/share/rez-packages/packages/nuke/15.1v1/nuke \
                -x \
                -t \
                -f \
                -X write_farm \
                -F 1051-1060 \
                "/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk" \
                "/data/share/AWSPortalRoot1/fixtures/nuke/out/test.####.exr"
        """
    )


class PluginNukeX_15_1v1(PluginNukeBase):
    plugin_type: Literal['PluginNukeX_15_1v1']

    executable: pathlib.Path = REZ_PACKAGES / "nuke" / "15.1v1" / "nukex"

    farm_command: str = textwrap.dedent(
        """
            ```shell
            /data/share/rez-packages/packages/nuke/15.1v1/nukex \
                -x \
                -i \
                -t \
                -f \
                -X write_farm \
                -F 1051-1060 \
                "/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk" \
                "/data/share/AWSPortalRoot1/fixtures/nuke/out/test.####.exr"
            ```
        """
    )

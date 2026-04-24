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

    # Farm command:
    # - husk --settings /Render/rendersettings --make-output-path --frame 1021 --frame-count 1 --frame-inc 1 --renderer BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output /data/share/AWSPortalRoot1/hello1.\$F4.exr --verbose CeT9 --usd-input /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
    # - /data/share/rez-packages/packages/houdini/19.5.805/husk --settings /Render/rendersettings --make-output-path --frame 1021 --frame-count 1 --frame-inc 1 --renderer BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output /data/share/AWSPortalRoot1/hello1.\$F4.exr --verbose ce9 --usd-input /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
    # - husk --settings /Render/rendersettings --make-output-path --frame 1021 --frame-count 1 --frame-inc 1 --renderer BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output /data/share/AWSPortalRoot1/hello1.\$F4.exr --verbose CeT9 /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
    #
    # -
    # - [OK] /data/share/rez-packages/packages/houdini/19.5.805/husk --settings /Render/rendersettings --make-output-path --frame 1021 --frame-count 10 --frame-inc 1 --renderer BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output \"/data/share/AWSPortalRoot1/out/Test Production/Shot/SH040/Rendering/002/raw/vivi_025.\\\$F4.exr\" --verbose ce9 --usd-input /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda

    # Not working
    # - /data/share/rez-packages/packages/houdini/19.5.805/husk --verbose ce9 --make-output-path --settings /Render/rendersettings --renderer BRAY_HdKarma --purpose ['geometry', 'render'] --frame 1006 --frame-count 1 --fps 25.0 --usd-input /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda --complexity veryhigh --output /data/share/AWSPortalRoot1/out/Test Production/Shot/SH040/Rendering/002/raw/vivi_025.\$F4.exr
    # - /data/share/rez-packages/packages/houdini/19.5.805/husk --settings /Render/rendersettings --make-output-path --frame 1021 --frame-count 1 --frame-inc 1 --renderer BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output "/data/share/AWSPortalRoot1/out/Test\ Production/Shot/SH040/Rendering/002/raw/vivi_025.$F4.exr" --verbose ce9 --usd-input /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "hrender"

    rop: str = Field(
        default="",
        description="The path to the render operator (ROP) to use "
                    "for rendering.",
    )


class PluginHoudiniKarma_19_5_805(PluginHoudiniKarmaBase):
    plugin_type: Literal['PluginHoudiniKarma_19_5_805']

    executable: pathlib.Path = REZ_PACKAGES /  "houdini" / "19.5.805" / "husk"

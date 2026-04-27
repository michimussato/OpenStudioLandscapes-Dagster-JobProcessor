import enum
import textwrap
from typing import List, Union

from pydantic import Field, computed_field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.plugin_base import PluginBase


class RenderEngine(enum.StrEnum):
    MANTRA = "MANTRA"
    KARMA = "BRAY_HdKarma"


class PluginHoudiniBase(PluginBase):
    pass


class PluginHoudiniHrenderBase(PluginBase):
    """
    `hrender` is the CLI deprecated Mantra render engine.
    It cannot be called directly without setting up the environment
    first (`houdini_setup`).

    Deadline uses some magic to do that by actually calling `hython` together
    with a proprietary script (`DeadlineRepository10/plugins/Houdini/hrender_dl.py`).

    References:
    - [hrender ](https://www.sidefx.com/docs/houdini/ref/utils/hrender.html)
    """

    args: List = [
        # DEADLINE_PLUGINS / "Houdini" / "hrender_dl.py",
        "-v",  # Run in verbose mode
        "-b", 1.0,  # Image processing fraction (0.01 to 1.0)
        "-e",
        "-f", "<STARTFRAME> <ENDFRAME>",  # with "-e":      -f start end    Frame range start and end
        "-i", "{chunk_size}",  # with "-e":      -i increment    Frame increment
        "-d", "{rop}",
        "-o", "'{render_output}'",
        "'{job_file}'",
    ]

    padding_command: str = "'$F' + str(EVAL_PADDING)"  # results in "$F4"


class Renderer(enum.StrEnum):
    BRAY_HdKarma = "BRAY_HdKarma"


class Complexity(enum.StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    veryhigh = "veryhigh"


class Purpose(enum.StrEnum):
    geometry = "geometry"
    guide = "guide"
    proxy = "proxy"
    render = "render"


class PluginHoudiniKarmaBase(PluginBase):
    """
    Karma (`husk`) is a native USD renderer, hence,
    its input (whether or not `--usd-input` was specified),
    needs to be a USD file (can be done using
    the `USD ROP`).

    Todo:
    - [ ] Maybe there is a commandline way to get from `.hip` to `.usd` directly; investigate.

    Applies to (non exhaustive):
    - 19.5

    References:
    - [Command Line Rendering in Houdini with Karma](https://deborahfowler.com/HoudiniResources/Overview-CommandLineRenderingKarma.html)
    """
    padding_command: str = "'$F' + str(EVAL_PADDING)"  # results in "$F4"

    args: List = [
        "--verbose", "{verbosity}",
        "--make-output-path",
        "--settings", "{settings}",
        "--renderer", "{renderer}",
        "--purpose", "{purpose_str}",
        # "--frame", "{cut_in}",
        "--frame", "<STARTFRAME>",
        # "--frame-count", "{cut_out - cut_in}",
        "--frame-count", str(1),
        # "--frame-inc", "{frame_inc}",
        "--fps", "{fps}",
        "--usd-input", "'{job_file}'",
        "--complexity", "{complexity}",
        "--output", "'{render_output}'",
    ]

    renderer: Renderer = Field(
        default=RenderEngine.KARMA.value,
    )

    complexity: Union[int, Complexity] = Field(
        default=Complexity.veryhigh.value,
        description=textwrap.dedent(
            """
            --complexity arg (=veryhigh)          Specify geometric complexity ({'low', 
                                                  'medium', 'high', 'veryhigh'} or a 
                                                  numeric value between 0 and 10)
            """
        )
    )

    purpose: List[Purpose] = Field(
        # default=f"{Purpose.geometry.value},{Purpose.render.value}",
        default=[
            Purpose.geometry.value,
            Purpose.render.value,
        ],
        description=textwrap.dedent(
            """
            --purpose arg (=geometry,render)      Specify the purpose for rendering.  
                                                  This is a comma separated list of 
                                                  purposes (from {'geometry', 'guide', 
                                                  'proxy', 'render'}).
            """
        )
    )

    @computed_field
    @property
    def purpose_str(self) -> str:
        return ",".join(self.purpose)

    settings: str = Field(
        description=textwrap.dedent(
            """
            -s [ --settings ] arg                 Render using properties defined by 
                                                  node.  You can specify a path relative 
                                                  to /Render.
            """
        )
    )

    verbosity: str = Field(
        default="Ce9",
        description=textwrap.dedent(
            """
            -V [ --verbose ] arg                  Render verbosity (e.g. -Va2)
                                                    0-9  Verbosity of rendering stats
                                                    p    Enable VEX profiling
                                                           (impacts performance)
                                                    P    Enable VEX profiling and NAN
                                                           checks (severe impact on
                                                           performance)
                                                    a/A  Turn on/off Alfred progress
                                                    c/C  Turn on/off colored messages
                                                    e/E  Turn on/off elapsed time stamps
                                                    t/T  Turn on/off message time stamps
            """
        )
    )
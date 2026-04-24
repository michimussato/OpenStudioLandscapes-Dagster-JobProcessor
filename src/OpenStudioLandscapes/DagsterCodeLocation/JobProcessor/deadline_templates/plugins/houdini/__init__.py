import enum
import pathlib
import textwrap
# from ssl import Purpose
from typing import List, Union

from pydantic import field_validator
from pydantic.fields import Field

# from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import DEADLINE_PLUGINS
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.plugin_base import PluginBase


class RenderEngine(enum.StrEnum):
    MANTRA = "CYCLES"
    KARMA = "KARMA"


# - Mantra
# - Karma (without -o)
# - hrender -v -e -f 1002 1003 -i 1 -d /stage/usdrender_rop_camera2 /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip
class PluginHoudiniBase(PluginBase):
    padding_command: str = "'\\$F' + str(EVAL_PADDING)"  # results in "$F4"
    # https://www.sidefx.com/docs/houdini/ref/utils/hrender.html
    # karma: https://deborahfowler.com/HoudiniResources/Overview-CommandLineRenderingKarma.html
    args: List = [
        # DEADLINE_PLUGINS / "Houdini" / "hrender_dl.py",
        "-v",  # Run in verbose mode
        "-b", 1.0,  # Image processing fraction (0.01 to 1.0)
        "-e",
        "-f", "<STARTFRAME> <ENDFRAME>",  # with "-e":      -f start end    Frame range start and end
        "-i", "{chunk_size}",  # with "-e":      -i increment    Frame increment
        "-d", "{rop}",
        "-o", "<QUOTE>{render_output}<QUOTE>",
        "<QUOTE>{job_file}<QUOTE>",
    ]

    # example_cmd: List[str] = [
    #     "hrender",
    #     "-v",
    #     "-e",
    #     "-f", "1001", "1010",
    #     "-i", "1",
    #     "-d", "/stage/usdrender_rop_camera2",
    #     "/data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.hip",
    # ]


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


# Solaris (export to USD first)
# - https://deborahfowler.com/HoudiniResources/Overview-CommandLineRenderingKarma.html
# - https://deborahrfowler.com/HoudiniResources/Overview-CommandLineRenderingKarma.html
# - usd_rop
#   - Example: /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
# - Karma
# - /data/share/tools/houdini-19.5.805-linux_x86_64_gcc9.3# husk -s --make-output-path -f 1010 -R BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output /data/share/AWSPortalRoot1/hello.$F4.exr -Vcet9 /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
# - /data/share/tools/houdini-19.5.805-linux_x86_64_gcc9.3# husk --settings /Render/rendersettings --make-output-path --frame 1021 --frame-count 1 --frame-inc 1 --renderer BRAY_HdKarma --purpose geometry,render --complexity veryhigh --snapshot 300 --output /data/share/AWSPortalRoot1/hello1.\$F4.exr --verbose CeT9 /data/share/AWSPortalRoot1/fixtures/houdini/project/vivi_025.usd_rop1.usda
class PluginHoudiniKarmaBase(PluginBase):
    padding_command: str = "'\\$F' + str(EVAL_PADDING)"  # results in "$F4"

    # example_cmd_husk: List[str] = [
    #     "husk",
    #     "--settings", "/Render/rendersettings",
    #     "--make-output-path",
    #     "--frame", "1001",
    #     "--renderer", "BRAY_HdKarma",
    #     "--purpose", "geometry,render",
    #     "--complexity", "veryhigh",
    #     "--snapshot", "300",
    #     "/tmp/houdini_temp/usd_renders/usdrender_1650_225_1/__render__.usd"
    # ]

    args: List = [
        "--verbose", "{verbosity}",
        "--settings", "{settings}",
        "--purpose", "{purpose}",
        # "--frame", "{cut_in}",
        "--frame", "<STARTFRAME>",
        # "--frame-count", "{cut_out - cut_in}",
        "--frame-count", str(1),
        # "--frame-inc", "{frame_inc}",
        "--fps", "{fps}",
        "--usd-input", "<QUOTE>{job_file}<QUOTE>",
        "--complexity", "{complexity}",
        "--output", "<QUOTE>{render_output}<QUOTE>",

        # "--render-format", "{output_format}",
        # # "--use-extension", "{use_extension}",
        # "--engine", "{render_engine}",
        # "--frame-start", "<STARTFRAME>",
        # "--frame-end", "<ENDFRAME>",
        # "--threads", "0",
        # "--render-anim",
        # "--",
        # "--cycles-print-stats",
    ]

    # help: str = Field(
    #     exclude=True,
    #     description=textwrap.dedent(
    #         """
    #         root@minion01:/data/share/tools/houdini-19.5.805-linux_x86_64_gcc9.3# husk --help
    #         Usage: husk [options] usdfile
    #         Build version: 19.5.805
    #
    #         Information:
    #           -h [ --help ]                         Show this help
    #           -v [ --version ]                      Print the renderer version
    #
    #         Karma Specific Options:
    #           --properties                          Print all rendering properties and
    #                                                 their defaults
    #           --property-definitions                Print full information about properties
    #                                                 (deprecated: please use
    #                                                 --property-definitions-file)
    #           --property-definitions-file arg       Print full information about properties
    #                                                 to the given file.If the filename is
    #                                                 '-', output will be written to stdout.
    #           --procedurals                         Print all procedural definitions
    #           --filters                             Print all filters/oracles
    #           --engine arg                          Choose rendering engine
    #           -p [ --pixel-samples ] arg (=128)     Samples per pixel
    #           --bucket-size arg (=128)              Bucket size
    #           --bucket-order arg (=middle)          Bucket render order (middle, top,
    #                                                 bottom, left, right)
    #           --image-mode arg (=bucket)            Image mode (progressive or bucket).
    #                                                 When this option is specified on the
    #                                                 command line, the progressive-passes is
    #                                                 always specified by the command line
    #                                                 option.
    #           --progressive-passes arg (=0)         When rendering in bucket mode, number
    #                                                 of progressive passes to run before
    #                                                 switching to bucket mode.
    #           --disable-lighting                    Disable all lighting
    #           --ao-samples arg (=1)                 Headlight shading: Ambient occlusion
    #                                                 samples
    #           --ao-distance arg (=1)                Headlight shading: Ambient occlusion
    #                                                 distance cutoff
    #           --lock-random arg (=0)                Lock the random number instead of using
    #                                                 the render frame
    #           --dicingcamera arg                    Dice from the specified camera. Uses
    #                                                 render camera if unspecified.
    #           --optimize-offline arg (=0)           Offline optimization level
    #                                                 This feature is currently disabled.
    #           --convergence-mode arg                Override integration method
    #                                                 'pathtraced': Maximum of 1 indirect ray
    #                                                 is generated per bounce.
    #                                                 'distributed': Per-component sampling
    #                                                 is enabled and the number of indirect
    #                                                 rays generated per BSDF component type
    #                                                 is user-controlled.
    #                                                 'variance': The number of indirect rays
    #                                                 is calculated based on initial noise
    #                                                 estimate, target noise threshold, and
    #                                                 the maximum number of camera rays.
    #           --baking-info                         Print out information about baking and
    #                                                 exit without rendering
    #
    #         USD Options:
    #           --usd-input arg                       The USD file for the scene
    #           --resolver-context arg                The file used to initialize the asset
    #                                                 resolver context for processing the
    #                                                 stage.
    #           --list-settings                       List all render settings primitives in
    #                                                 the USD file
    #           --list-cameras                        List all cameras in the USD file
    #           --list-renderers                      List all Hydra render delegates
    #           --purpose arg (=geometry,render)      Specify the purpose for rendering.
    #                                                 This is a comma separated list of
    #                                                 purposes (from {'geometry', 'guide',
    #                                                 'proxy', 'render'}).
    #           --complexity arg (=veryhigh)          Specify geometric complexity ({'low',
    #                                                 'medium', 'high', 'veryhigh'} or a
    #                                                 numeric value between 0 and 10)
    #           --mask arg                            Limit stage population to these prims,
    #                                                 their descendants and ancestors.To
    #                                                 specify multiple paths, use either
    #                                                 commas or spaces.
    #           --disable-scene-materials             Disable scene materials.  This applies
    #                                                 to all render delegates.
    #           --disable-scene-lights                Disable scene lights.  This applies to
    #                                                 all render delegates.
    #           --disable-motionblur                  Override any render settings and
    #                                                 disable motion blur
    #           --disable-delegate-products           Disable delegate render products
    #                                                 (non-raster render products)
    #           -s [ --settings ] arg                 Render using properties defined by
    #                                                 node.  You can specify a path relative
    #                                                 to /Render.
    #           --prerender-script arg                Python script to edit the stage right
    #                                                 before render.  Use the 'stage'
    #                                                 variable to access the render stage in
    #                                                 the Python script.
    #           --preframe-script arg                 Python script to edit the stage before
    #                                                 each frame is rendered. Use the 'stage'
    #                                                 variable to access the render stage in
    #                                                 the Python script.
    #           --postframe-script arg                Python script to edit the stage after
    #                                                 each frame is rendered. Use the 'stage'
    #                                                 variable to access the render stage in
    #                                                 the Python script.
    #           --postrender-script arg               Python script to edit the stage after
    #                                                 all frames are rendered. Use the
    #                                                 'stage' variable to access the render
    #                                                 stage in the Python script.
    #           --allowed-procedurals arg (=basic)    Control which procedurals should be
    #                                                 allowed to contribute to the final USD
    #                                                 stage. Valid options are:
    #                                                   'none'  - no procedurals
    #                                                   'basic' - graph procedurals that only
    #                                                             generate curves and points
    #                                                   'all'   - all procedurals (may
    #                                                             require Houdini Engine
    #                                                             license)
    #           --capture-procedurals                 Save the result of any expanded
    #                                                 procedurals
    #           --procedurals-capture-directory arg (=/tmp/houdini_temp)
    #                                                 Directory to store expanded procedurals
    #           --usd-trace arg                       Enable USD tracing.  This should be a
    #                                                 comma separated list of reports to
    #                                                 generate from the list below:
    #                                                   'report' - times and sample counts
    #                                                   'timing' - time in function
    #                                                   'chrome' - Save trace viewer output
    #                                                             (see usd-chrome-file)
    #                                                 Note: this uses the husktrace Python
    #                                                 script in $HH
    #           --usd-chrome-file arg                 Enable USD function tracing and save
    #                                                 the JSON output to the given file.
    #                                                 Note that if this option is used it
    #                                                 automatically enables '--usd-trace
    #                                                 chrome'.
    #
    #         Render Settings Overrides:
    #           -c [ --camera ] arg                   Render from the specified camera
    #           -o [ --output ] arg                   Output image.  Variables are expanded
    #                                                 in the string can be represented in
    #                                                 various ways:
    #                                                   - $F, $FF $F4:  Current frame number
    #                                                   - $N:  The N'th frame in the sequence
    #                                                   - <F>, <FF>, <F4>:  Frame UDIM style
    #                                                   - %d, %g, %04d:  Frame printf style
    #                                                 A comma separated list of filenames can
    #                                                 be used to override images when there
    #                                                 are multiple render products.
    #           -r [ --res ] arg                      Image resolution (e.g. '--res 1280
    #                                                 720')
    #           -S [ --res-scale ] arg (=100)         Scale the output resolution by the
    #                                                 given percentage
    #           --pixel-aspect arg (=1)               Pixel aspect ratio
    #           --make-output-path                    Create path to the output image if it
    #                                                 doesn't already exist.
    #
    #         MPlay Settings Overrides:
    #           --mplay-monitor arg                   Automatically start up an mplay monitor
    #                                                 of this render using the comma
    #                                                 separated list of AOV planes (i.e.
    #                                                 'C,diffuse'). Specifying '-' as the AOV
    #                                                 list will monitor all AOVs.
    #           --mplay-scale arg (=100)              A scale to apply to any mplay render
    #                                                 (between 10 and 100). This affects both
    #                                                 the monitor and any product that
    #                                                 renders to mplay
    #           --no-mplay                            Disable any rendering to mplay.  This
    #                                                 option is useful when rendering on
    #                                                 headless machines (on a farm)
    #           --mplay-update arg (=0.5)             Number of seconds between mplay updates
    #           --mplay-session arg                   The mplay session label
    #           --mplay-bgimage arg                   Specify a background image for mplay
    #           --mplay-remotehost arg                Specify a remote host and socket port
    #                                                 (hostname:port) to connect to for
    #                                                 display
    #           --mplay-gamma arg (=0)                If the value is greater than 0, this
    #                                                 will be used as the display gamma value
    #                                                 in mplay
    #           --mplay-lut arg                       Specify a display LUT for mplay
    #
    #         Frame Range:
    #           -f [ --frame ] arg (=1)               The start frame for rendering
    #           -n [ --frame-count ] arg (=1)         The number of frames to render
    #           -i [ --frame-inc ] arg (=1)           The frame increment
    #           --fps arg (=24)                       Override the frames per second defined
    #                                                 on the stage.
    #
    #         Rendering:
    #           -R [ --renderer ] arg                 Choose an specific Hydra head
    #           --delegate-options arg                An option to pass delegate specific
    #                                                 command line arguments
    #           -j [ --threads ] arg (=0)             Thread count:
    #                                                   '-j 0' use all processors
    #                                                   '-j 4' use four processors
    #                                                   '-j -1' use all but one processors
    #           --fast-exit arg (=2)                  0 - Force a full tear down of the
    #                                                     USD scene and Hydra
    #                                                 1 - Fast exit lets the OS tear down
    #                                                     resources
    #                                                 2 - Use setting in UsdRenderers.json
    #                                                     to use delegate preference
    #           --restart-delegate arg (=0)           Restart the render delegate every N
    #                                                 frames instead of using USD deltas
    #           --snapshot arg (=-1)                  Snapshot partial image after this
    #                                                 number of seconds.
    #           --snapshot-path arg                   Path to write snapshot to.
    #           --snapshot-suffix arg (=_part)        Snapshot suffix to add to the image
    #                                                 filename.
    #           --snapshot-save-mode arg (=off)       Normally snapshots are removed when the
    #                                                 render completes.
    #                                                  off    - Remove snapshots when done.
    #                                                  number - Save numbered sequence of
    #                                                           snapshots.
    #
    #           --exrmode arg (=1)                    OpenEXR saving mode:
    #                                                  -1 Use HOUDINI_OIIO_EXR variable
    #                                                   0 Classic driver (HOUDINI_OIIO_EXR=0)
    #                                                   1 Modern driver (HOUDINI_OIIO_EXR=1)
    #
    #           --autocrop arg                        Pattern of AOVs to be considered when
    #                                                 computing the data windowfor
    #                                                 auto-cropping
    #           --tile-count arg                      Number of tiles in the x and y axis
    #                                                 respectively
    #           --tile-index arg (=0)                 Index of the tile to render (0 indexed)
    #           --tile-suffix arg                     A suffix to add to the tiled output
    #                                                 name. Supports variable expansion like
    #                                                 the -o option (e.g. '_tile%02d')
    #           --timelimit arg (=-1)                 Limit rendering time to this number of
    #                                                 seconds
    #           --timelimit-image                     Time limit applies to images rather
    #                                                 than the whole sequence
    #           --timelimit-nosave-partial            If time limit is exceeded, do not save
    #                                                 partial results
    #           --stdout arg                          Write standard output to the given file
    #           --stderr arg                          Write standard error to the given file
    #           --append-stdout arg                   Append standard output to the given
    #                                                 file
    #           --append-stderr arg                   Append standard error to the given file
    #           --windows-console arg                 Windows only: open a console for output
    #                                                 (none|wait|nowait)
    #           -V [ --verbose ] arg                  Render verbosity (e.g. -Va2)
    #                                                   0-9  Verbosity of rendering stats
    #                                                   p    Enable VEX profiling
    #                                                          (impacts performance)
    #                                                   P    Enable VEX profiling and NAN
    #                                                          checks (severe impact on
    #                                                          performance)
    #                                                   a/A  Turn on/off Alfred progress
    #                                                   c/C  Turn on/off colored messages
    #                                                   e/E  Turn on/off elapsed time stamps
    #                                                   t/T  Turn on/off message time stamps
    #
    #         Licensing Options:
    #           --check-licenses arg                  Enable licenses to check. List any
    #                                                 licenses
    #                                                 that should be enabled when requesting
    #                                                 licenses.
    #                                                 The internal name for the license must
    #                                                 be used.
    #           --skip-licenses arg                   Disable licenses to check. List any
    #                                                 licenses
    #                                                 that should be skipped when requesting
    #                                                 licenses.
    #                                                 The internal name for the license must
    #                                                 be used.
    #           --list-license-checks                 List the licensing information
    #           --skip-license-modes                  License modes that should be skipped
    #                                                 when requesting a license.
    #                                                  - 'commercial': Skip all licenses that
    #                                                 are commercial licenses.
    #                                                  - 'education': Skip all education
    #                                                 licenses.
    #                                                  - 'indie': Skip all indie licenses.
    #                                                  - 'apprentice': Skip all apprentice
    #                                                 licenses.
    #           --check-license-modes                 License modes that should be checked
    #                                                 when requseting a license.
    #                                                  - 'commercial': Enable all commercial
    #                                                 licenses.
    #                                                  - 'education': Enable all education
    #                                                 licenses.
    #                                                  - 'indie': Enable all indie licenses.
    #                                                  - 'apprentice': Enable all apprentice
    #                                                 licenses.
    #           --license-release-delay               Use this option to add a delay to when
    #                                                 hserver will release the
    #                                                 license once the application is no
    #                                                 longer using the license.
    #           --license-max-seat-hold               Use this option to specify the maximum
    #                                                 time this application should hold a
    #                                                 license seat for. A new license seat is
    #                                                 retrieved when the max seat hold
    #                                                 occurs. This is a handy option when you
    #                                                 want to ensure artists don't use a
    #                                                 given license for longer then they
    #                                                 should.
    #           --apprentice                          Force a tainted apprentice session.
    #           --indie                               Force an indie session.
    #           --core                                Force a core session.
    #           --pdg                                 [Deprecated] Go into legacy PDG mode
    #                                                 when requesting a license.
    #
    #         Note:
    #             Redirecting stdout/stderr to 'consolewait' or 'consolenowait'
    #             will open a console window for output on Windows.
    #
    #         Note:
    #             Sending the husk process a USR1 signal will trigger saving a
    #             snapshot image
    #         """
    #     ),
    # )

    # cut_in: int = Field(
    #     description="The start frame for rendering",
    #     alias="cut_in"
    # )
    #
    # cut_out: int = Field(
    #     description="The start frame for rendering",
    #     alias="cut_in"
    # )

    # frame_count: int = Field(
    #     default=1,
    #     description="The number of frames to render",
    # )

    # @property
    # def cut_out(self):
    #     return self.frame + self.frame_count - 1

    # frame_inc: int = Field(
    #     default=1,
    #     description="The frame increment",
    # )

    # fps: float = Field(
    #     default=24.0,
    #     description="Override the frames per second defined on the stage.",
    # )

    # usd_input: pathlib.Path = Field(
    #     description="The USD file for the scene",
    # )

    # disable_motion_blur: bool = Field(
    #     default=False,
    #     description="Override any render settings and disable motion blur",
    # )

    # disable_scene_materials: bool = Field(
    #     default=False,
    #     description="Disable scene materials. This applies to "
    #                 "all render delegates.",
    # )

    # disable_scene_lights: bool = Field(
    #     default=False,
    #     description="Disable scene lights. This applies to "
    #                 "all render delegates.",
    # )

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

    @field_validator("purpose")
    @classmethod
    def concat_purpose(cls, v: List[Purpose]) -> str:
        return ",".join(v)

    settings: str = Field(
        # default="/Render/rendersettings",
        description=textwrap.dedent(
            """
            -s [ --settings ] arg                 Render using properties defined by 
                                                  node.  You can specify a path relative 
                                                  to /Render.
            """
        )
    )

    # output: pathlib.Path = Field(
    #     description=textwrap.dedent(
    #         """
    #         -o [ --output ] arg                   Output image.  Variables are expanded
    #                                               in the string can be represented in
    #                                               various ways:
    #                                                 - $F, $FF $F4:  Current frame number
    #                                                 - $N:  The N'th frame in the sequence
    #                                                 - <F>, <FF>, <F4>:  Frame UDIM style
    #                                                 - %d, %g, %04d:  Frame printf style
    #                                               A comma separated list of filenames can
    #                                               be used to override images when there
    #                                               are multiple render products.
    #         """
    #     ),
    # )

    verbosity: str = Field(
        default="ce9",
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
import enum
from typing import List

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.plugin_base import PluginBase


class RenderEngine(enum.StrEnum):
    CYCLES = "CYCLES"
    BLENDER_EEVEE = "BLENDER_EEVEE"
    WORKBENCH = "WORKBENCH"


class CyclesDevices(enum.StrEnum):
    # maybe there is a dynamic way
    # that also supports indexing
    """
    Cycles Render Options:
            Cycles add-on options must be specified following a double dash.

    --cycles-device <device>
            Set the device used for rendering.
            Valid options are: 'CPU' 'CUDA' 'OPTIX' 'HIP' 'ONEAPI' 'METAL'.

            Append +CPU to a GPU device to render on both CPU and GPU.

            Example:
            # blender -b file.blend -f 20 -- --cycles-device OPTIX
    --cycles-print-stats
            Log statistics about render memory and time usage.
    """
    CPU = "CPU"
    CUDA = "CUDA"
    CUDA_CPU = "CUDA+CPU"
    OPTIX = "OPTIX"
    OPTIX_CPU = "OPTIX+CPU"
    HIP = "HIP"
    HIP_CPU = "HIP+CPU"
    ONEAPI = "ONEAPI"
    ONEAPI_CPU = "ONEAPI+CPU"
    METAL = "METAL"
    METAL_CPU = "METAL+CPU"


class OutputFormatsBlender(enum.StrEnum):
    TGA = "TGA"
    RAWTGA = "RAWTGA"
    JPEG = "JPEG"
    IRIS = "IRIS"
    AVIRAW ="AVIRAW"
    AVIJPEG = "AVIJPEG"
    PNG = "PNG"
    BMP = "BMP"
    HDR = "HDR"
    TIFF = "TIFF"
    EXR = "EXR"
    OPEN_EXR = "EXR"
    OPEN_EXR_MULTILAYER = "EXR"
    FFMPEG = "FFMPEG"
    CINEON = "CINEON"
    DPX = "DPX"
    JP2 = "JP2"
    WEBP = "WEBP"


class UseExtension(enum.StrEnum):
    TRUE = "1"
    FALSE = "0"


class PluginBlenderBase(PluginBase):
    """
    -o or --render-output <path>
        Set the render path and file name.
        Use '//' at the start of the path to render relative to the blend-file.

        The '#' characters are replaced by the frame number, and used to define zero padding.

        * 'animation_##_test.png' becomes 'animation_01_test.png'
        * 'test-######.png' becomes 'test-000001.png'

        When the filename does not contain '#', the suffix '####' is added to the filename.

        The frame number will be added at the end of the filename, eg:
        # blender -b animation.blend -o //render_ -F PNG -x 1 -a
        '//render_' becomes '//render_####', writing frames as '//render_0001.png'

    """
    args: List = [
        "--enable-autoexec",
        "--background",
        "'{job_file}'",
        "--render-output", "'{render_output}'",
        # "--render-format", "{output_format.upper()}",
        # AttributeError: 'str' object has no attribute 'upper()'
        #   File "/opt/python3.11/lib/python3.11/site-packages/dagster/_core/execution/plan/utils.py", line 56, in op_execution_error_boundary
        #     yield
        #   File "/opt/python3.11/lib/python3.11/site-packages/dagster/_utils/__init__.py", line 480, in iterate_with_context
        #     next_output = next(iterator)
        #                   ^^^^^^^^^^^^^^
        #   File "/opt/python3.11/lib/python3.11/site-packages/OpenStudioLandscapes/DagsterCodeLocation/JobProcessor/dagster_job_processor/assets/read_yaml.py", line 1898, in render_arguments
        #     ret = " ".join(args).format(
        #           ^^^^^^^^^^^^^^^^^^^^^^
        "--render-format", "{output_format}",
        # "--use-extension", "{use_extension}",
        "--engine", "{render_engine}",
        "--frame-start", "<STARTFRAME>",
        "--frame-end", "<ENDFRAME>",
        "--threads", "0",
        "--render-anim",
        "--",
        "--cycles-print-stats",
    ]

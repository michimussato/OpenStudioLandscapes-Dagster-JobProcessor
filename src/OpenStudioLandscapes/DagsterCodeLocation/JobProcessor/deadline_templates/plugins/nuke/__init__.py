from typing import List

from pydantic import Field, computed_field

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.plugin_base import PluginBase



# plugin["submitter"]["args"].append('<QUOTE>\\\"{render_output}\\\"<QUOTE>')


class PluginNukeBase(PluginBase):
    """
    -X option
    --------------------------------------------------------------
    This argument specifies the output of the write_farm node.
    Write nodes are able to take extra arguments i.e. like this:
    WriteNode.file: [argv 0]/write_farm/[argv 1].####.[argv 2] etc.
    So, [argv <index>]
    write_farm.file has "[argv 0]" as value (as of now),
    so the last argument of this args must be the full, absolute
    path of the final image.

    This allows to specify the output from commandline.
    However, this needs a special Write Node that
    reads the `sysargv` to redirect the output.

    If a write node is expecting an argument that was
    not specified, the error would look somehow
    like this:
    ```
    Missing command-line argument #2 for write_farm.file
    ```
    """
    args: List = [
        # "--nukex",
        "-x",
        "-t",  # terminal only (no gui); if <script> is a .py file it will be executed
        "-f",  # render at full size (turns off proxy; use -p to force render at proxy)
        # "-X", f'{",".join(job["write_nodes"])}'
        # Todo:
        #  - [ ] maybe add a switch to skip `-X` if no write_nodes are specified
        "-X", "{write_nodes_str}",
        "-F", "<STARTFRAME>-<ENDFRAME>",  # if bool(job["write_nodes"])
        "'{job_file}'",
        "'{render_output}'"
    ]

    write_nodes: List[str] = Field(
        default_factory=list,
        description="List of Nuke write nodes to write execute.",
    )

    @computed_field
    @property
    def write_nodes_str(self) -> str:
        if not bool(self.write_nodes):
            return "''"
        else:
            return ",".join(self.write_nodes)

import pathlib
import textwrap
from typing import Literal

from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins import *
from OpenStudioLandscapes.DagsterCodeLocation.JobProcessor.deadline_templates.plugins.nuke import PluginNukeBase


"""
=======================================================
Error
=======================================================
Error: FailRenderException : Process returned non-zero exit code '1'
   at Deadline.Plugins.DeadlinePlugin.FailRender(String message) (Python.Runtime.PythonException)
  File "/var/lib/Thinkbox/Deadline10/workers/minion01-deadline-10-2-worker/plugins/69ef34be2158848ea22ad045/CommandLine.py", line 79, in RenderTasks
    self.FailRender( "Process returned non-zero exit code '{}'".format( exitCode ) )
   at Python.Runtime.Dispatcher.Dispatch(ArrayList args)
   at __FranticX_GenericDelegate0Dispatcher.Invoke()
   at Deadline.Plugins.DeadlinePlugin.RenderTasks()
   at Deadline.Plugins.DeadlinePlugin.DoRenderTasks()
   at Deadline.Plugins.PluginWrapper.RenderTasks(Task task, String& outMessage, AbortLevel& abortLevel)
   at Deadline.Plugins.PluginWrapper.RenderTasks(Task task, String& outMessage, AbortLevel& abortLevel)

=======================================================
Type
=======================================================
RenderPluginException

=======================================================
Stack Trace
=======================================================
   at Deadline.Plugins.SandboxedPlugin.d(DeadlineMessage bgt, CancellationToken bgu)
   at Deadline.Plugins.SandboxedPlugin.RenderTask(Task task, CancellationToken cancellationToken)
   at Deadline.Slaves.SlaveRenderThread.c(TaskLogWriter ajy, CancellationToken ajz)

=======================================================
Log
=======================================================
2026-04-27 10:11:10:  0: Loading Job's Plugin timeout is Disabled
2026-04-27 10:11:10:  0: SandboxedPlugin: Render Job As User disabled, running as current user 'root'
2026-04-27 10:11:15:  0: Executing plugin command of type 'Initialize Plugin'
2026-04-27 10:11:15:  0: INFO: Executing plugin script '/var/lib/Thinkbox/Deadline10/workers/minion01-deadline-10-2-worker/plugins/69ef34be2158848ea22ad045/CommandLine.py'
2026-04-27 10:11:15:  0: INFO: Plugin execution sandbox using Python version 3
2026-04-27 10:11:15:  0: INFO: Single Frames Only: False
2026-04-27 10:11:15:  0: INFO: About: Command Line Plugin for Deadline
2026-04-27 10:11:15:  0: INFO: The job's environment will be merged with the current environment before rendering
2026-04-27 10:11:15:  0: Done executing plugin command of type 'Initialize Plugin'
2026-04-27 10:11:16:  0: Start Job timeout is disabled.
2026-04-27 10:11:16:  0: Task timeout is disabled.
2026-04-27 10:11:16:  0: Loaded job: No Show - No Entity Name - No Task Name - fixture_v001.nk - 003 - nuke (69ef34be2158848ea22ad045)
2026-04-27 10:11:16:  0: Executing plugin command of type 'Start Job'
2026-04-27 10:11:16:  0: DEBUG: S3BackedCache Client is not installed.
2026-04-27 10:11:16:  0: INFO: Executing global asset transfer preload script '/var/lib/Thinkbox/Deadline10/workers/minion01-deadline-10-2-worker/plugins/69ef34be2158848ea22ad045/GlobalAssetTransferPreLoad.py'
2026-04-27 10:11:16:  0: INFO: Looking for legacy (pre-10.0.26) AWS Portal File Transfer...
2026-04-27 10:11:16:  0: INFO: Looking for legacy (pre-10.0.26) File Transfer controller in /opt/Thinkbox/S3BackedCache/bin/task.py...
2026-04-27 10:11:16:  0: INFO: Could not find legacy (pre-10.0.26) AWS Portal File Transfer.
2026-04-27 10:11:16:  0: INFO: Legacy (pre-10.0.26) AWS Portal File Transfer is not installed on the system.
2026-04-27 10:11:16:  0: Done executing plugin command of type 'Start Job'
2026-04-27 10:11:16:  0: Plugin rendering frame(s): 1037-1046
2026-04-27 10:11:16:  0: Executing plugin command of type 'Render Task'
2026-04-27 10:11:16:  0: INFO: Executable: /data/share/rez-packages/packages/nuke/15.1v1/nuke
2026-04-27 10:11:16:  0: INFO: Arguments: -t -f -F 1037-1046 -x '/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk' '/data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/003/raw/fixture_v001.####.exr'
2026-04-27 10:11:16:  0: INFO: Execute in Shell: False
2026-04-27 10:11:16:  0: INFO: Invoking: Run Process
2026-04-27 10:11:16:  0: STDOUT: Using Rez Wrapper: /data/share/rez-packages/packages/nuke/15.1v1/nuke
2026-04-27 10:11:16:  0: STDOUT: Name: nuke
2026-04-27 10:11:16:  0: STDOUT: Version: 15.1v1
2026-04-27 10:11:16:  0: STDOUT: Extra Args: -t -f -F 1037-1046 -x '/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk' '/data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/003/raw/fixture_v001.####.exr'
2026-04-27 10:11:18:  0: STDOUT: Nuke 15.1v1, 64 bit, built Jun  6 2024.
2026-04-27 10:11:18:  0: STDOUT: Copyright (c) 2024 The Foundry Visionmongers Ltd.  All Rights Reserved.
2026-04-27 10:11:19:  0: STDOUT: [10:11.18] Warning: Autosave file for /data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk is newer
2026-04-27 10:11:19:  0: STDOUT: Missing command-line argument #2 for write_farm_small.file
2026-04-27 10:11:19:  0: INFO: Process returned: 1
2026-04-27 10:11:19:  0: Done executing plugin command of type 'Render Task'

=======================================================
Details
=======================================================
Date: 04/27/2026 10:11:22
Frames: 1037-1046
Elapsed Time: 00:00:00:12
Job Submit Date: 04/27/2026 10:04:46
Job User: michael
Average RAM Usage: 1382137856 (9%)
Peak RAM Usage: 1549762560 (10%)
Average CPU Usage: 36%
Peak CPU Usage: 67%
Used CPU Clocks (x10^6 cycles): 18277
Total CPU Clocks (x10^6 cycles): 50769

=======================================================
Worker Information
=======================================================
Worker Name: minion01-deadline-10-2-worker
Version: v10.2.1.1 Release (094cbe890)
Operating System: Linux
Machine User: root
IP Address: 192.168.178.16
MAC Address: 00:E0:4C:30:42:FD
CPU Architecture: x86_64
CPUs: 4
CPU Usage: 18%
Memory Usage: 1.3 GB / 15.5 GB (8%)
Free Disk Space: 11.968 GB 
Video Card: 
"""


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

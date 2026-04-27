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

"""
=======================================================
Error
=======================================================
Error: FailRenderException : Process returned non-zero exit code '100'
   at Deadline.Plugins.DeadlinePlugin.FailRender(String message) (Python.Runtime.PythonException)
  File "/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69ef3ea72158848ea22ad04c/CommandLine.py", line 79, in RenderTasks
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
2026-04-27 10:47:42:  0: Loading Job's Plugin timeout is Disabled
2026-04-27 10:47:42:  0: SandboxedPlugin: Render Job As User disabled, running as current user 'root'
2026-04-27 10:47:47:  0: Executing plugin command of type 'Initialize Plugin'
2026-04-27 10:47:47:  0: INFO: Executing plugin script '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69ef3ea72158848ea22ad04c/CommandLine.py'
2026-04-27 10:47:47:  0: INFO: Plugin execution sandbox using Python version 3
2026-04-27 10:47:47:  0: INFO: Single Frames Only: False
2026-04-27 10:47:47:  0: INFO: About: Command Line Plugin for Deadline
2026-04-27 10:47:47:  0: INFO: The job's environment will be merged with the current environment before rendering
2026-04-27 10:47:47:  0: Done executing plugin command of type 'Initialize Plugin'
2026-04-27 10:47:47:  0: Start Job timeout is disabled.
2026-04-27 10:47:47:  0: Task timeout is disabled.
2026-04-27 10:47:47:  0: Loaded job: No Show - No Entity Name - No Task Name - fixture_v001.nk - 004 - nuke (69ef3ea72158848ea22ad04c)
2026-04-27 10:47:47:  0: Executing plugin command of type 'Start Job'
2026-04-27 10:47:47:  0: DEBUG: S3BackedCache Client is not installed.
2026-04-27 10:47:47:  0: INFO: Executing global asset transfer preload script '/var/lib/Thinkbox/Deadline10/workers/minion04-deadline-10-2-worker/plugins/69ef3ea72158848ea22ad04c/GlobalAssetTransferPreLoad.py'
2026-04-27 10:47:47:  0: INFO: Looking for legacy (pre-10.0.26) AWS Portal File Transfer...
2026-04-27 10:47:47:  0: INFO: Looking for legacy (pre-10.0.26) File Transfer controller in /opt/Thinkbox/S3BackedCache/bin/task.py...
2026-04-27 10:47:47:  0: INFO: Could not find legacy (pre-10.0.26) AWS Portal File Transfer.
2026-04-27 10:47:47:  0: INFO: Legacy (pre-10.0.26) AWS Portal File Transfer is not installed on the system.
2026-04-27 10:47:47:  0: Done executing plugin command of type 'Start Job'
2026-04-27 10:47:47:  0: Plugin rendering frame(s): 997-1006
2026-04-27 10:47:47:  0: Executing plugin command of type 'Render Task'
2026-04-27 10:47:47:  0: INFO: Executable: /data/share/rez-packages/packages/nuke/15.1v1/nuke
2026-04-27 10:47:47:  0: INFO: Arguments: -x -t -f -X write_farm -F 997-1006 '/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk' '/data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.####.exr'
2026-04-27 10:47:47:  0: INFO: Execute in Shell: False
2026-04-27 10:47:47:  0: INFO: Invoking: Run Process
2026-04-27 10:47:47:  0: STDOUT: Using Rez Wrapper: /data/share/rez-packages/packages/nuke/15.1v1/nuke
2026-04-27 10:47:47:  0: STDOUT: Name: nuke
2026-04-27 10:47:47:  0: STDOUT: Version: 15.1v1
2026-04-27 10:47:47:  0: STDOUT: Extra Args: -x -t -f -X write_farm -F 997-1006 '/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk' '/data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.####.exr'
2026-04-27 10:47:49:  0: STDOUT: Nuke 15.1v1, 64 bit, built Jun  6 2024.
2026-04-27 10:47:49:  0: STDOUT: Copyright (c) 2024 The Foundry Visionmongers Ltd.  All Rights Reserved.
2026-04-27 10:47:49:  0: STDOUT: A license for nuke was not found
2026-04-27 10:47:49:  0: STDOUT: FOUNDRY LICENSE ERROR REPORT
2026-04-27 10:47:49:  0: STDOUT: ----------------------------
2026-04-27 10:47:49:  0: STDOUT: Timestamp: Mon Apr 27 10:47:49 2026
2026-04-27 10:47:49:  0: STDOUT: License(s) Requested:
2026-04-27 10:47:49:  0: STDOUT: nuke 2024.0606 render only with options all 
2026-04-27 10:47:49:  0: STDOUT: Extended Info: 
2026-04-27 10:47:49:  0: STDOUT: Host : minion04
2026-04-27 10:47:49:  0: STDOUT: System ID(s) : 9add6e386d16 , 3e389486e6f1 , 363a988e8e2d , da595ce05e41 , d6c549f21824
2026-04-27 10:47:49:  0: STDOUT: RLM Environment Info : /usr/local/foundry/RLM
2026-04-27 10:47:49:  0: STDOUT: Login Environment Info : /root/.local/share/Foundry/Tokens
2026-04-27 10:47:49:  0: STDOUT: RLM LICENSE DIAGNOSTICS
2026-04-27 10:47:49:  0: STDOUT: nuke : Bad server hostname in license file or port@host ENT_STATUS_RLM_LICENSE_BADHOST
2026-04-27 10:47:49:  0: STDOUT: License Paths(s) : /usr/local/foundry/RLM
2026-04-27 10:47:49:  0: STDOUT: LOGIN LICENSE DIAGNOSTICS
2026-04-27 10:47:49:  0: STDOUT: nuke : No tokens found for product ENT_STATUS_TEND_TOKEN_NO_PRODUCT
2026-04-27 10:47:49:  0: STDOUT: License Paths(s) : /root/.local/share/Foundry/Tokens
2026-04-27 10:47:49:  0: INFO: Process returned: 100
2026-04-27 10:47:49:  0: Done executing plugin command of type 'Render Task'

=======================================================
Details
=======================================================
Date: 04/27/2026 10:47:53
Frames: 997-1006
Elapsed Time: 00:00:00:11
Job Submit Date: 04/27/2026 10:47:03
Job User: michael
Average RAM Usage: 1627493248 (10%)
Peak RAM Usage: 1647607808 (10%)
Average CPU Usage: 34%
Peak CPU Usage: 56%
Used CPU Clocks (x10^6 cycles): 4837
Total CPU Clocks (x10^6 cycles): 14225

=======================================================
Worker Information
=======================================================
Worker Name: minion04-deadline-10-2-worker
Version: v10.2.1.1 Release (094cbe890)
Operating System: Linux
Machine User: root
IP Address: 192.168.178.19
MAC Address: 9A:DD:6E:38:6D:16
CPU Architecture: x86_64
CPUs: 4
CPU Usage: 27%
Memory Usage: 1.5 GB / 15.5 GB (9%)
Free Disk Space: 12.328 GB 
Video Card: 
"""

"""
=======================================================
Log
=======================================================
2026-04-27 10:47:39:  0: Loading Job's Plugin timeout is Disabled
2026-04-27 10:47:39:  0: SandboxedPlugin: Render Job As User disabled, running as current user 'root'
2026-04-27 10:47:44:  0: Executing plugin command of type 'Initialize Plugin'
2026-04-27 10:47:44:  0: INFO: Executing plugin script '/var/lib/Thinkbox/Deadline10/workers/minion01-deadline-10-2-worker/plugins/69ef3ea72158848ea22ad04c/CommandLine.py'
2026-04-27 10:47:44:  0: INFO: Plugin execution sandbox using Python version 3
2026-04-27 10:47:44:  0: INFO: Single Frames Only: False
2026-04-27 10:47:44:  0: INFO: About: Command Line Plugin for Deadline
2026-04-27 10:47:44:  0: INFO: The job's environment will be merged with the current environment before rendering
2026-04-27 10:47:44:  0: Done executing plugin command of type 'Initialize Plugin'
2026-04-27 10:47:44:  0: Start Job timeout is disabled.
2026-04-27 10:47:44:  0: Task timeout is disabled.
2026-04-27 10:47:44:  0: Loaded job: No Show - No Entity Name - No Task Name - fixture_v001.nk - 004 - nuke (69ef3ea72158848ea22ad04c)
2026-04-27 10:47:44:  0: Executing plugin command of type 'Start Job'
2026-04-27 10:47:44:  0: DEBUG: S3BackedCache Client is not installed.
2026-04-27 10:47:44:  0: INFO: Executing global asset transfer preload script '/var/lib/Thinkbox/Deadline10/workers/minion01-deadline-10-2-worker/plugins/69ef3ea72158848ea22ad04c/GlobalAssetTransferPreLoad.py'
2026-04-27 10:47:45:  0: INFO: Looking for legacy (pre-10.0.26) AWS Portal File Transfer...
2026-04-27 10:47:45:  0: INFO: Looking for legacy (pre-10.0.26) File Transfer controller in /opt/Thinkbox/S3BackedCache/bin/task.py...
2026-04-27 10:47:45:  0: INFO: Could not find legacy (pre-10.0.26) AWS Portal File Transfer.
2026-04-27 10:47:45:  0: INFO: Legacy (pre-10.0.26) AWS Portal File Transfer is not installed on the system.
2026-04-27 10:47:45:  0: Done executing plugin command of type 'Start Job'
2026-04-27 10:47:45:  0: Plugin rendering frame(s): 1077-1086
2026-04-27 10:47:45:  0: Executing plugin command of type 'Render Task'
2026-04-27 10:47:45:  0: INFO: Executable: /data/share/rez-packages/packages/nuke/15.1v1/nuke
2026-04-27 10:47:45:  0: INFO: Arguments: -x -t -f -X write_farm -F 1077-1086 '/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk' '/data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.####.exr'
2026-04-27 10:47:45:  0: INFO: Execute in Shell: False
2026-04-27 10:47:45:  0: INFO: Invoking: Run Process
2026-04-27 10:47:45:  0: STDOUT: Using Rez Wrapper: /data/share/rez-packages/packages/nuke/15.1v1/nuke
2026-04-27 10:47:45:  0: STDOUT: Name: nuke
2026-04-27 10:47:45:  0: STDOUT: Version: 15.1v1
2026-04-27 10:47:45:  0: STDOUT: Extra Args: -x -t -f -X write_farm -F 1077-1086 '/data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk' '/data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.####.exr'
2026-04-27 10:47:47:  0: STDOUT: Nuke 15.1v1, 64 bit, built Jun  6 2024.
2026-04-27 10:47:47:  0: STDOUT: Copyright (c) 2024 The Foundry Visionmongers Ltd.  All Rights Reserved.
2026-04-27 10:47:47:  0: STDOUT: [10:47.47] Warning: Autosave file for /data/share/AWSPortalRoot1/fixtures/nuke/fixture_v001.nk is newer
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1077.exr took 0.13 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1077 (1 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1078.exr took 0.13 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1078 (2 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1079.exr took 0.11 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1079 (3 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1080.exr took 0.13 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1080 (4 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1081.exr took 0.13 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1081 (5 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1082.exr took 0.13 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1082 (6 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1083.exr took 0.12 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1083 (7 of 10)
2026-04-27 10:47:48:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1084.exr took 0.12 seconds
2026-04-27 10:47:48:  0: STDOUT: Frame 1084 (8 of 10)
2026-04-27 10:47:49:  0: STDOUT: .2
2026-04-27 10:47:49:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1085.exr took 0.12 seconds
2026-04-27 10:47:49:  0: STDOUT: Frame 1085 (9 of 10)
2026-04-27 10:47:49:  0: STDOUT: Writing /data/share/AWSPortalRoot1/out/No Show/No Entity Type/No Entity Name/No Task Name/004/raw/fixture_v001.1086.exr took 0.11 seconds
2026-04-27 10:47:49:  0: STDOUT: Frame 1086 (10 of 10)
2026-04-27 10:47:49:  0: STDOUT: Total render time: 1.26 seconds
2026-04-27 10:47:49:  0: INFO: Process returned: 0
2026-04-27 10:47:49:  0: Done executing plugin command of type 'Render Task'

=======================================================
Details
=======================================================
Date: 04/27/2026 10:47:50
Frames: 1077-1086
Job Submit Date: 04/27/2026 10:47:03
Job User: michael
Average RAM Usage: 129627136 (1%)
Peak RAM Usage: 130072576 (1%)
Average CPU Usage: 20%
Peak CPU Usage: 34%
Used CPU Clocks (x10^6 cycles): 873
Total CPU Clocks (x10^6 cycles): 4361

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
CPU Usage: 25%
Memory Usage: 1.3 GB / 15.5 GB (8%)
Free Disk Space: 11.945 GB 
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

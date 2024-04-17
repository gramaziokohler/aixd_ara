from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas._os
from ghpythonlib.componentbase import executingcomponent as component
from scriptcontext import sticky as st

from aixd_grasshopper.constants import DEFAULT_PORT

try:
    from subprocess import PIPE
    from subprocess import Popen
except ImportError:
    from System.Diagnostics import Process

import os

import aixd_grasshopper as ag


class ApiRunner(object):
    def __init__(
        self,
        package=None,
        python=None,
        url="http://127.0.0.1",
        port=DEFAULT_PORT,
        service=None,
        max_conn_attempts=100,
        autoreload=True,
        capture_output=True,
        path=None,
        working_directory=None,
    ):
        self.python = compas._os.select_python(python)
        self.service = "aixd_grasshopper.api"
        self.working_directory = working_directory
        self.capture_output = capture_output
        self.port = port

        self.start_server()

    def start_server(self):
        env = compas._os.prepare_environment()

        try:
            Popen

        except NameError:
            self._process = Process()
            for name in env:
                if self._process.StartInfo.EnvironmentVariables.ContainsKey(name):
                    self._process.StartInfo.EnvironmentVariables[name] = env[name]
                else:
                    self._process.StartInfo.EnvironmentVariables.Add(name, env[name])
            self._process.StartInfo.UseShellExecute = True
            self._process.StartInfo.RedirectStandardOutput = self.capture_output
            self._process.StartInfo.RedirectStandardError = self.capture_output
            self._process.StartInfo.FileName = self.python
            self._process.StartInfo.Arguments = "-m {0} {1}".format(self.service, self.port)
            self._process.Start()
        else:
            args = [self.python, "-m", self.service, str(self.port)]

            kwargs = dict(env=env)
            print(args)
            if self.capture_output:
                kwargs["stdout"] = PIPE
                kwargs["stderr"] = PIPE
            if self.working_directory:
                kwargs["cwd"] = self.working_directory

            self._process = Popen(args, **kwargs)

    def stop_server(self):
        print("Stopping the server proxy.")
        self._terminate_process()

    def _terminate_process(self):
        """Attempts to terminate the python process hosting the proxy server.

        The process reference might not be present, e.g. in the case
        of reusing an existing connection. In that case, this is a no-op.
        """
        if not self._process:
            return
        try:
            self._process.terminate()
        except Exception:
            pass
        try:
            self._process.kill()
        except Exception:
            pass


api_path = os.path.dirname(ag.__file__)

print(api_path)


def create_api_runner_id(component):
    name = "api-runner"
    return "{}_{}".format(name, component.InstanceGuid)


class ApiRunnerComponent(component):

    def RunScript(self, start, stop, show_window):
        key = create_api_runner_id(self)
        if not show_window:
            show_window = True  # default

        port = DEFAULT_PORT

        if not start:
            return None
        if show_window:
            python = "python"
            capture_output = False
        else:
            python = "pythonw"
            capture_output = True

        if stop:
            self.stop_previous(key)

        if start:
            self.stop_previous(key)
            runner = ApiRunner(python=python, port=port, capture_output=capture_output, working_directory=api_path)
            st[key] = runner

        runner = st[key]

        return runner

    def stop_previous(self, key):
        # stop previous API runner if any
        previous_api_runner = st.get(key)
        if previous_api_runner:
            previous_api_runner.stop_server()
            st.pop(key)

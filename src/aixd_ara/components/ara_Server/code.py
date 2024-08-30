from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import urllib2

import compas
import compas._os
from ghpythonlib.componentbase import executingcomponent as component
from scriptcontext import sticky as st

from aixd_ara.constants import DEFAULT_PORT

try:
    from subprocess import PIPE
    from subprocess import Popen
except ImportError:
    from System.Diagnostics import Process

import os

import aixd_ara as ag


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
        show_window=False,
        path=None,
        working_directory=None,
    ):
        self.python = compas._os.select_python(python)
        self.service = "aixd_ara.api"
        self.working_directory = working_directory
        self.show_window = show_window
        self.port = port

        self.start_process()

    def start_process(self):
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
            self._process.StartInfo.RedirectStandardOutput = not self.show_window
            self._process.StartInfo.RedirectStandardError = not self.show_window
            self._process.StartInfo.FileName = self.python
            self._process.StartInfo.Arguments = "-m {0} {1}".format(self.service, self.port)
            self._process.Start()
        else:
            args = [self.python, "-m", self.service, str(self.port)]
            kwargs = dict(env=env)

            if self.show_window:
                if compas.is_mono():
                    python_command = " ".join(args)
                    apple_script = """
                    tell application "Terminal"
                        do script "{}"
                        activate
                    end tell
                    """.format(
                        python_command
                    )
                    args = ["osascript", "-e", apple_script]
            else:
                kwargs["stdout"] = PIPE
                kwargs["stderr"] = PIPE

            if self.working_directory:
                kwargs["cwd"] = self.working_directory
            self._process = Popen(args, **kwargs)

    def stop_process(self):
        """Attempts to terminate the python process hosting the proxy server.

        The process reference might not be present, e.g. in the case
        of reusing an existing connection. In that case, this is a no-op.
        """
        print("Stopping the server process.")

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

    def RunScript(self, start, stop, show_window=True):
        key = create_api_runner_id(self)
        port = DEFAULT_PORT

        if show_window:
            python = "python"
        else:
            python = "pythonw"

        if start:
            self.stop(key)
            runner = ApiRunner(python=python, port=port, show_window=show_window, working_directory=api_path)
            st[key] = runner

        if stop:
            self.stop(key)

    def stop(self, key):
        # Attempt gracefully stopping the server
        try:
            urllib2.urlopen("http://127.0.0.1:8765/shutdown", timeout=1)
        except Exception:
            pass

        # stop previous API runner if any
        previous_api_runner = st.get(key)
        if previous_api_runner:
            try:
                previous_api_runner.stop_process()
            except Exception as e:
                print("Unable to stop previous process")
                print(e)
            st.pop(key)
        else:
            print("No previous process runner found")

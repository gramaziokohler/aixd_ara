"""Reveals the folder in the file explorer."""
# flake8: noqa

import compas
import subprocess

if open:
    command = "open"
    if compas.is_windows():
        command = "explorer"

    subprocess.Popen([command, path])

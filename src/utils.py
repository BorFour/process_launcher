import sys
import os
import subprocess
from enum import Enum
from pathlib import Path

from PyQt5.QtWidgets import (QFileDialog)

class AppMode(Enum):
    LAUNCH = 0
    EDIT = 1


class ProcessStatus(Enum):
    STOPPED = 0
    RUNNING = 1


class SupportedPlatforms(Enum):
    LINUX = 0
    WINDOWS = 1
    MACOS = 2
    UNKNOWN = 3

    @classmethod
    def get_platform(cls, platform_name):
        if "linux" in platform_name:
            return cls.LINUX
        elif "windows" in platform_name:
            return cls.WINDOWS
        elif "macos" in platform_name or "darwin" in platform_name:
            return cls.MACOS
        else:
            return cls.UNKNOWN


def get_platform():
    return SupportedPlatforms.get_platform(sys.platform)

def get_home_folder():
    return str(Path.home())

def get_config_folder():
    return os.path.join(get_home_folder(), '.process_launcher')

def clearLayout(layout):
    """Deletes the widget in a layout."""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

def browse_existing_directory(widget, dialog_text) -> str:
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename = str(QFileDialog.getExistingDirectory(widget, dialog_text, options=options))
    return filename


def kill_command_windows(pid):
    """Popen.kill doesn't actually work on Windows."""
    dev_null = open(os.devnull, 'w')
    command = ['TASKKILL', '/F', '/T', '/PID', str(pid)]
    subprocess.Popen(command, stdin=dev_null,
                     stdout=sys.stdout, stderr=sys.stderr)


def parse_dropped_file(text: str) -> str:
    platform = get_platform()
    if platform == SupportedPlatforms.LINUX:
        text = text.replace("file://", "")
    elif platform == SupportedPlatforms.WINDOWS:
        text = text.replace("file:///", "")

    return text


my_path = os.path.abspath(os.path.dirname(__file__))

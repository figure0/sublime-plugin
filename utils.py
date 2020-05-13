import os
import platform
import re
import sublime
import subprocess

from .consts import WARNING, ERROR, INFO, MAC_OS_BIN_PATHS, LINUX_BIN_PATHS
from .settings import get_custom_python_path
from .session import set_is_python_version_valid

CLI_STARTER = """
# -*- coding: utf-8 -*-
import re
import sys
from deepcode.cli import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
"""


def is_global_python_version_compatible(python_command="python3"):
    try:
        with subprocess.Popen(
            [python_command, "-V"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=platform.system() == "Windows",
        ) as proc:
            [major, minor, patch] = [
                int(x)
                for x in re.search(
                    r"Python\s*([\d.]+)", proc.stdout.read().decode("utf-8")
                )
                .group(1)
                .split(".")
            ]
            if major < 3 or minor < 6 or (minor == 6 and patch < 5):
                raise Exception("Global Python version has to be 3.6.5 or higher")
        set_is_python_version_valid(True)
        return True
    except Exception as e:
        if python_command == "python3":
            return is_global_python_version_compatible(python_command="python")
        sublime.error_message(
            "This plugin requires python >= 3.6.5. If you want to use a virtual python environment, please adjust package setting 'customPythonPath'"
        )
        return False


def patch_local_deepcode(python_command="python3"):
    try:
        CWD = os.path.dirname(os.path.realpath(__file__))
        subprocess.call(
            [python_command, "-m", "pip", "install", "-U", "pip"],
            shell=platform.system() == "Windows",
        )
        subprocess.call(
            [
                python_command,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--no-deps",
                "-r",
                "requirements.txt",
                "-t",
                ".{}lib".format(os.path.sep),
            ],
            cwd=CWD,
            shell=platform.system() == "Windows",
        )
        with open(
            "{0}{1}lib{1}deepcode{1}__main__.py".format(CWD, os.path.sep), "w"
        ) as f:
            f.write(CLI_STARTER)
    except Exception as e:
        if python_command == "python3":
            return patch_local_deepcode(python_command="python")
        print("path local deepcode exception: ", e)
        sublime.error_message(
            "There was an error installing/upgrading deepcode scripts"
        )


def merge_two_lists(fst, snd):
    return fst + list(set(snd) - set(fst))


def fix_python_path_if_needed():
    if platform.system() == "Darwin":
        updated_paths = ":".join(
            merge_two_lists(MAC_OS_BIN_PATHS, os.environ["PATH"].split(":"))
        )
        os.environ["PATH"] = updated_paths
    elif platform.system() == "Linux":
        updated_paths = ":".join(
            merge_two_lists(LINUX_BIN_PATHS, os.environ["PATH"].split(":"))
        )
        os.environ["PATH"] = updated_paths

    custom_python_path = get_custom_python_path()
    if custom_python_path:
        os.environ["PATH"] = "{}:{}".format(os.environ["PATH"], custom_python_path)


def find(point, errors):
    for p in errors:
        if point in p.get("region"):
            return p


def get_severity_status_string(severity):
    if severity == WARNING:
        return "   ⚠️"
    elif severity == ERROR:
        return "   ⛔"
    else:
        return "   ⓘ"


def get_error_count(error_info, message):
    if error_info[ERROR] > 0:
        message += "⛔ {} ".format(error_info[ERROR])
    if error_info[WARNING] > 0:
        message += "⚠️ {} ".format(error_info[WARNING])
    if error_info[INFO] > 0:
        message += "ⓘ {} ".format(error_info[INFO])
    return message

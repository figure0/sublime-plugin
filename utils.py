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

custom_env = os.environ.copy()
custom_env["LC_CTYPE"] = "en_US.UTF-8"
custom_env["LC_ALL"] = "en_US.UTF-8"
custom_env["LANG"] = "en_US.UTF-8"


def get_env():
    return custom_env

def get_python_command(python_command="python3"):
    try:
        with subprocess.Popen(
            [python_command, "-V"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=platform.system() == "Windows",
            env=get_env()
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
        return python_command
    except Exception as e:
        if python_command == "python3":
            return get_python_command(python_command="python")
        sublime.error_message(
            "DeepCodeAI plugin requires python >= 3.6.5. If you want to use a virtual python environment, please adjust package setting 'customPythonPath'"
        )


def get_pip_command(python_command):
    commands = [
        [python_command, "-m", "pip3", "-V"],
        [python_command, "-m", "pip", "-V"],
        ["pip3", "-V"],
        ["pip", "-V"],
    ]

    def get_pip(comand_index=0):
        try:
            with subprocess.Popen(
                commands[comand_index],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=platform.system() == "Windows",
                env=get_env()
            ) as proc:
                res = re.findall(
                    r"pip ([\d|\.]+).*", proc.stdout.read().decode("utf-8")
                )
                if len(res) > 0:
                    return commands[comand_index][:-1]

                raise Exception("pip error")
        except Exception as e:
            if comand_index == len(commands) - 1:
                sublime.error_message(
                    "DeepCodeAI plugin requires you to have python pip globally available. \n\nFor more instructions visit: \nhttps://pip.pypa.io/en/stable/installing"
                )
            elif comand_index < len(commands) - 1:
                return get_pip(comand_index=comand_index + 1)

    return get_pip()


def patch_local_deepcode(pip_command):
    CWD = os.path.dirname(os.path.realpath(__file__))
    lib_dir = os.path.join(sublime.cache_path(), 'deepcode_lib')
    print('sublime.cache_path() --> {}'.format(lib_dir))
    print('pip_command --> {}'.format(pip_command))
    print('get_env --> {}'.format(get_env()))

    try:
        subprocess.call(
            pip_command
            + [
                "install",
                "--upgrade",
                "--no-deps",
                "-r",
                "requirements.txt",
                "-t",
                lib_dir
            ],
            cwd=CWD,
            shell=platform.system() == "Windows",
            env=get_env()
        )

        with open(os.path.join(lib_dir, 'deepcode', '__main__.py'), "w") as f:
            f.write(CLI_STARTER)

    except Exception as e:
        print("path local deepcode exception: ", e)
        sublime.error_message(
            "There was an error installing/upgrading DeepCodeAI scripts"
        )


def merge_two_lists(fst, snd):
    return fst + list(set(snd) - set(fst))

def fix_python_path_if_needed():
    if platform.system() == "Darwin":
        updated_paths = ":".join(
            merge_two_lists(MAC_OS_BIN_PATHS, os.environ["PATH"].split(":"))
        )
        custom_env["PATH"] = updated_paths
    elif platform.system() == "Linux":
        updated_paths = ":".join(
            merge_two_lists(LINUX_BIN_PATHS, os.environ["PATH"].split(":"))
        )
        custom_env["PATH"] = updated_paths

    custom_python_path = get_custom_python_path()
    if custom_python_path:
        custom_env["PATH"] = "{}:{}".format(os.environ["PATH"], custom_python_path)


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

fix_python_path_if_needed()


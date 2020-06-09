import os
import platform
import re
import sublime
import subprocess

from .consts import WARNING, ERROR, INFO, CLI_DEPENDENCY
from .settings import get_custom_python_path
from .session import set_is_python_version_valid

custom_env = {} # os.environ.copy()
custom_env["LC_CTYPE"] = "en_US.UTF-8"
custom_env["LC_ALL"] = "en_US.UTF-8"
custom_env["LANG"] = "en_US.UTF-8"


def get_env():
    return custom_env

def get_default_python_command():
    commands = ['python', 'python3']

    for python_command in commands:
        try:
            with subprocess.Popen(
                [python_command, "-V"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=platform.system() == "Windows",
                env=custom_env
            ) as proc:
                [major, minor, patch] = [
                    int(x)
                    for x in re.search(
                        r"Python\s*([\d.]+)", proc.stdout.read().decode("utf-8")
                    ).group(1).split(".")
                ]
                
                if major * 100 + minor * 10 + patch < 365: # minimal version is 3.6.5
                    # raise Exception("Global Python version has to be 3.6.5 or higher")
                    pass
                else:
                    set_is_python_version_valid(True)
                    return python_command
        except Exception as e:
            pass
    
    sublime.error_message(
        "DeepCodeAI plugin requires python >= 3.6.5. If you want to use a virtual python environment, please adjust package setting 'customPythonPath'"
    )

python_command = get_default_python_command()

def get_pip_command():
    commands = [
        [python_command, "-m", "pip", "-V"],
        [python_command, "-m", "pip3", "-V"],
        ["pip", "-V"],
        ["pip3", "-V"],
    ]

    for pip_command in commands:
        try:
            with subprocess.Popen(
                pip_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=platform.system() == "Windows",
                env=custom_env
            ) as proc:
                res = re.findall(
                    r"pip ([\d|\.]+).*", proc.stdout.read().decode("utf-8")
                )
                if len(res) > 0:
                    return pip_command[:-1] # like python -m pip
        except Exception as e:
            pass
    
    sublime.error_message(
        "DeepCodeAI plugin requires you to have python pip globally available. \n\nFor more instructions visit: \nhttps://pip.pypa.io/en/stable/installing"
    )


def install_cli():
    if not python_command:
        return
    pip_command = get_pip_command()
    if not pip_command:
        return

    cache_path = sublime.cache_path()
    lib_dir = os.path.join(cache_path, 'deepcode_lib')
    
    try:
        subprocess.check_call(
            ['mkdir', '-p', 'deepcode_lib'],
            cwd=cache_path,
            shell=platform.system() == "Windows"
        )

        subprocess.check_call(
            pip_command
            + [
                "install",
                CLI_DEPENDENCY,
                "-t",
                lib_dir
            ],
            cwd=cache_path,
            shell=platform.system() == "Windows",
            env=custom_env
        )

    except Exception as e:
        print("path local deepcode exception: ", e)
        sublime.error_message(
            "There was an error installing/upgrading DeepCodeAI scripts"
        )


def merge_two_lists(fst, snd):
    return fst + list(set(snd) - set(fst))

def fix_python_path_if_needed():
    if platform.system() == "Darwin":
        pass
    elif platform.system() == "Linux":
        # updated_paths = ":".join(
        #     merge_two_lists(LINUX_BIN_PATHS, os.environ["PATH"].split(":"))
        # )
        # custom_env["PATH"] = updated_paths
        pass

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


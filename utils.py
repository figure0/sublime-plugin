import os
import platform
import re
import sublime
import subprocess

from .consts import WARNING, ERROR, INFO, CLI_DEPENDENCY, LINUX_BIN_PATHS, MAC_OS_BIN_PATHS
from .settings import get_python_command, set_python_command

def get_custom_env_path():
    os_paths = []
    if platform.system() == 'Darwin':
        os_paths = MAC_OS_BIN_PATHS
    elif platform.system() == 'Linux':
        os_paths = LINUX_BIN_PATHS
    
    return ':'.join([os.environ['PATH']] + os_paths)

def get_custom_env():
    custom_env = dict(os.environ.copy(), **{
        'LC_CTYPE': 'en_US.UTF-8',
        'LC_ALL': 'en_US.UTF-8',
        'LANG': 'en_US.UTF-8',
        'PATH': get_custom_env_path()
    })
    print('custom env --> {}'.format(custom_env))
    return custom_env

def get_default_python_command():
    commands = ['python', 'python3']

    default_args = dict(
        stderr=subprocess.PIPE,
        shell=platform.system() == 'Windows',
        env=get_custom_env()
    )
    
    for python_command in commands:
        try:
            version_output = subprocess.check_output(
                [python_command, '-V'],
                **default_args
            ).decode('utf-8')
            print('command: {} | version_output: {}'.format(python_command, version_output))
            [major, minor, patch] = [
                int(x)
                for x in re.search(r'Python\s*([\d.]+)', version_output).group(1).split('.')
            ]
            py_version = major * 100 + minor * 10 + patch
            if py_version > 365: # minimal version is 3.6.5
                return python_command
        except Exception as e:
            pass

def get_pip_command():
    python_command = get_python_command()
    commands = [
        [python_command, '-m', 'pip', '-V'],
        [python_command, '-m', 'pip3', '-V'],
        ['pip', '-V'],
        ['pip3', '-V'],
    ]

    default_args = dict(
        stderr=subprocess.PIPE,
        shell=platform.system() == 'Windows',
        env=get_custom_env()
    )

    for pip_command in commands:
        try:
            version_output = subprocess.check_output(pip_command, **default_args).decode('utf-8')
            print('command: {} | version_output: {}'.format(pip_command, version_output))
            res = re.findall(r'pip ([\d|\.]+).*', version_output)
            if len(res) > 0:
                return pip_command[:-1] # like python -m pip
        except Exception as e:
            pass


def install_cli():
    python_command = get_python_command()
    if not python_command:
        python_command = get_default_python_command()
        if not python_command:
            sublime.error_message(
                "DeepCodeAI plugin requires python >= 3.6.5. If you want to use a virtual python environment, please adjust package setting 'python'"
            )
            return
        
        set_python_command(python_command)
    
    pip_command = get_pip_command()
    if not pip_command:
        sublime.error_message(
            "DeepCodeAI plugin requires you to have python pip globally available. \n\nFor more instructions visit: \nhttps://pip.pypa.io/en/stable/installing"
        )
        return

    cache_path = sublime.cache_path()
    lib_dir = os.path.join(cache_path, 'deepcode_lib')
    
    try:
        default_args = dict(
            stderr=subprocess.PIPE,
            cwd=cache_path,
            shell=platform.system() == 'Windows',
            env=get_custom_env()
        )
        # Make directory for our dependencies
        subprocess.check_call(
            ['mkdir', '-p', 'deepcode_lib'],
            **default_args
        )
        
        # Upgrade pip
        subprocess.check_call(
            pip_command + ['install', '-U', 'pip'],
            **default_args
        )

        subprocess.check_call(
            pip_command
            + [
                'install',
                CLI_DEPENDENCY,
                '-t',
                lib_dir
            ],
            **default_args
        )

    except Exception as e:
        print('path local deepcode exception: ', e)
        sublime.error_message(
            'There was an error installing/upgrading DeepCodeAI scripts'
        )


def find(point, errors):
    for p in errors:
        if point in p.get('region'):
            return p


def get_severity_status_string(severity):
    if severity == WARNING:
        return '   ⚠️'
    elif severity == ERROR:
        return '   ⛔'
    else:
        return '   ⓘ'


def get_error_count(error_info, message):
    if error_info[ERROR] > 0:
        message += '⛔ {} '.format(error_info[ERROR])
    if error_info[WARNING] > 0:
        message += '⚠️ {} '.format(error_info[WARNING])
    if error_info[INFO] > 0:
        message += 'ⓘ {} '.format(error_info[INFO])
    return message



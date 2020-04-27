import os
import re
import sublime
import subprocess

from .consts import WARNING, ERROR, INFO

CLI_STARTER = """
# -*- coding: utf-8 -*-
import re
import sys
from deepcode.cli import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
"""

def is_global_python_version_compatible():
    try:
        with subprocess.Popen(['python3', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            [major, minor, patch] = [int(x) for x in re.search(r'Python\s*([\d.]+)', proc.stdout.read().decode('utf-8')).group(1).split('.')]
            if major < 3 or minor < 6 or (minor == 6 and patch < 5):
                raise Exception('Global Python version has to be 3.6 or higher')
        return True
    except Exception as e:
        print('Python version exception', e)
        sublime.error_message('Global Python version has to be 3.6 or higher')
        return False

def patch_local_deepcode():
    try:
        CWD = os.path.dirname(os.path.realpath(__file__))
        subprocess.call(['python3', '-m', 'pip', 'install', '-U', 'pip'])
        subprocess.call(['python3', '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt', '-t', './lib'], cwd=CWD)
        subprocess.call(['rm', '-rf', './lib/asyncio'], cwd=CWD)
        with open("{}/lib/deepcode/__main__.py".format(CWD), 'w') as f:
            f.write(CLI_STARTER)
    except Exception as e:
        print('path local deepcode exception: ', e)
        sublime.error_message('There was an error installing/upgrading deepcode scripts')

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

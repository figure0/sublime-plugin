import io
import json
import os
import re
import sublime
import subprocess
from threading import Timer

from .consts import AUTH_TIMEOUT
from .progress import handle_progress_update
from .settings import get_service_url, get_linters_enabled, set_token, get_token
from .statuses import set_status

PERCENT = '([A-Za-z]+.*%)\\|'
FILE = '(\\w+.*)f \\['

def terminate_login(view, proc):
    proc.kill()
    set_status(view, 'DeepCode: 🚫 Unauthorized')

def login(view):
    continue_with_login = sublime.ok_cancel_dialog(
        'Use your GitHub, Bitbucket or GitLab account to authenticate with DeepCode', 'Login')
    if continue_with_login:
        set_status(view, 'DeepCode: Please, complete login process in opened browser.')
        with deepcode('--service-url', get_service_url(), 'login') as proc:
            t = Timer(AUTH_TIMEOUT, lambda: terminate_login(view, proc))
            t.start()
            resp = re.findall(r'(\w+) has been saved.', proc.stdout.read().decode('utf-8'))
            t.cancel()
            return resp[0] if len(resp) > 0 else None


def authenticate(view):
    token = login(view)
    if token is None:
        return
    set_token(token)
    sublime.set_timeout_async(lambda: view.window().run_command('deepcode_analyze'), 0)


def deepcode(*args):
    MODULE_DIR = "{}/lib".format(os.path.dirname(os.path.realpath(__file__)))
    return subprocess.Popen(['python', '-m', 'deepcode'] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            cwd=MODULE_DIR)


def analyze(project_path, view):
    args = ['--service-url', get_service_url(), '--api-key', get_token(), 'analyze', '--path',
            project_path]
    if get_linters_enabled():
        args.append('--with-linters')

    try:
        proc = deepcode(*args)

        progress_data = io.TextIOWrapper(proc.stderr, encoding="utf-8")
        handle_progress_update(progress_data, view)

        data = io.TextIOWrapper(proc.stdout, encoding="utf-8").read()
        parsedData = json.loads(data)

        results = parsedData.get('results')
        url = parsedData.get('url')

        for k, v in results.items():
            if k == 'files':
                for deepcode_relpath, pv in v.items():
                    v[project_path + deepcode_relpath.split(project_path.split('/')[-1])[-1]] = v.pop(deepcode_relpath)

        return [results, url]
    except Exception as e:
        print(str(e))
        if str(e) == "Unauthorized":
            set_status(view, 'DeepCode: 🚫 Unauthorized')
            authenticate(view)
        elif str(e) == "Server Unavailable":
            set_status(view, 'DeepCode: 🚧 Service Unavailable')
            proc.kill()
        else:
            print('SOMETHING UNEXPECTED', e)
            set_status(view, 'DeepCode: ❌ Project Analyze Failed')

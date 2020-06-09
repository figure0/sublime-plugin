import io
import json
import os
import platform
import re
import sublime
import subprocess
from threading import Timer

from .consts import AUTH_TIMEOUT
from .progress import handle_progress_update
from .settings import get_service_url, get_linters_enabled, set_token, get_token, get_python_command
from .statuses import set_status
from .utils import get_custom_env

def terminate_login(view, proc):
    proc.kill()
    set_status(view, "DeepCode: 🚫 Unauthorized")


def login(view):

    def cli_login():
        with deepcode(
            "--service-url",
            get_service_url(),
            "--source",
            "sublime",
            "login"
        ) as proc:
            error = proc.stderr.read().decode("utf-8")
            print("LOGIN ERROROR", error, bool(error))
            if bool(error):
                proc.kill()
                raise "Login Failed"
            t = Timer(AUTH_TIMEOUT, lambda: terminate_login(view, proc))
            t.start()
            resp = re.findall(
                r"(\w+) has been saved.", proc.stdout.read().decode("utf-8")
            )
            t.cancel()
            return resp[0] if len(resp) > 0 else None

    continue_with_login = sublime.ok_cancel_dialog(
        "Use your GitHub, Bitbucket or GitLab account to authenticate with DeepCode",
        "Login",
    )
    if continue_with_login:
        set_status(view, "DeepCode: Please, complete login process in opened browser.")
        return cli_login()


def authenticate(view):
    token = login(view)
    if token is None:
        return
    set_token(token)
    sublime.set_timeout_async(lambda: view.window().run_command("deepcode_analyze"), 0)


def deepcode(*args):
    MODULE_DIR = os.path.join(sublime.cache_path(), 'deepcode_lib')
    return subprocess.Popen(
        [get_python_command(), os.path.join("bin", "deepcode")] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=MODULE_DIR,
        shell=platform.system() == "Windows",
        env=dict(get_custom_env(), PYTHONPATH=MODULE_DIR)
    )


def analyze(project_path, view):
    args = [
        "--service-url",
        get_service_url(),
        "--api-key",
        get_token(),
        "analyze",
        "--path",
        project_path,
    ]
    if get_linters_enabled():
        args.append("--with-linters")

    try:
        proc = deepcode(*args)
        progress_data = io.TextIOWrapper(proc.stderr, encoding="utf-8")
        handle_progress_update(progress_data, view)

        data = io.TextIOWrapper(proc.stdout, encoding="utf-8").read()
        parsedData = json.loads(data)

        results = parsedData.get("results")
        if platform.system() == "Windows":
            results = {
                k: {k1.replace("/", "\\"): v1 for k1, v1 in v.items()}
                for k, v in results.items()
            }
        url = parsedData.get("url")

        project_name = project_path.split(os.path.sep)[-1]
        file_issues = {}
        for k, v in results.items():
            if k == "files":
                for deepcode_relpath, pv in v.items():
                    file_issues[project_path + deepcode_relpath] = pv

        results["files"] = file_issues
        return [results, url]
    except Exception as e:
        print(str(e))
        if str(e) == "Unauthorized":
            set_status(view, "DeepCode: 🚫 Unauthorized")
            authenticate(view)
        elif str(e) == "Server Unavailable":
            set_status(view, "DeepCode: 🚧 Service Unavailable")
            proc.kill()
        else:
            print("SOMETHING UNEXPECTED", e)
            set_status(view, "DeepCode: ❌ Project Analyze Failed")

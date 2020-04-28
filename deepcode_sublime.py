import os
import sublime
import sublime_plugin


from .utils import (
    is_global_python_version_compatible,
    patch_local_deepcode,
    fix_python_path_if_needed,
)
from .settings import set_initial_settings_if_needed

os.environ["LC_CTYPE"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ["LANG"] = "en_US.UTF-8"
os.environ["PATH"] = "/usr/bin"


def plugin_loaded():
    fix_python_path_if_needed()
    if not is_global_python_version_compatible():
        return
    patch_local_deepcode()
    set_initial_settings_if_needed()


class Deepcode(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        view.window().run_command("deepcode_analyze", {"on_save": True})

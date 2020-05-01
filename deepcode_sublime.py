import os
import sublime
import sublime_plugin


from .utils import (
    is_global_python_version_compatible,
    patch_local_deepcode,
    fix_python_path_if_needed,
)
from .settings import set_initial_settings_if_needed
from .session import (
    is_initial_analysis_runned_for_project,
    add_project_to_initial_analysis_runned_list,
)

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
    def analyze_project_on_load(self):
        for w in sublime.windows():
            if len(w.folders()) == 0:
                return
            elif not is_initial_analysis_runned_for_project(w.folders()[0]):
                print("INITIAL_ANALYSIS")
                sublime.set_timeout_async(
                    lambda: w.run_command("deepcode_analyze"), 1000
                )
                add_project_to_initial_analysis_runned_list(w.folders()[0])

    def on_activated_async(self, view):
        sublime.set_timeout_async(lambda: self.analyze_project_on_load(), 0)

    def on_post_save_async(self, view):
        view.window().run_command("deepcode_analyze", {"on_save": True})

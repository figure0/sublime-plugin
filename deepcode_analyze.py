import sublime
import sublime_plugin

from .analyze import analyze, authenticate
from .connection import is_connected_to_internet
from .highlight import highlight_errors, clear_previous_highlight
from .panels import show_results_in_panel
from .persist import DB
from .settings import get_token, get_consented, set_consented
from .statuses import set_status
from .session import add_project_to_asked_to_consent, is_python_version_valid, user_asked_to_consent_for_project


def run_analysis(view, on_save = False):
    if not is_connected_to_internet():
        set_status(view, 'DeepCode: ❌ No Internet Connection  ')
        return

    if not view.window() or len(view.window().folders()) == 0:
        return
    
    if not is_python_version_valid():
        return

    project_path = view.window().folders()[0]

    if get_token() is None:
        authenticate(view)

    token = get_token()
    if token is None:
        return
    if project_path not in get_consented():
        set_status(view, 'DeepCode: Not activated for this project 🔐  ')
        if on_save and user_asked_to_consent_for_project(project_path):
            return
        consented = sublime.ok_cancel_dialog('Do you consent for DeepCode to analyzing your project?', 'Yes')
        add_project_to_asked_to_consent(project_path)
        if not consented:
            return
        set_consented(project_path)

    set_status(view, 'DeepCode: Analyzing... ⏳ ')
    results = analyze(project_path, view)
    if results:
        DB[project_path] = results[0]
        sublime.set_timeout_async(lambda: show_results_in_panel(view, DB[project_path], results[1]))
        sublime.set_timeout_async(lambda: highlight_errors(view))


class DeepcodeAnalyzeCommand(sublime_plugin.WindowCommand):
    def run(self, on_save=False):
        sublime.set_timeout_async(lambda: clear_previous_highlight(self.window.active_view()), 10)
        sublime.set_timeout_async(lambda: run_analysis(self.window.active_view(), on_save), 100)

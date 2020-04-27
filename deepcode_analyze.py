import sublime
import sublime_plugin

from .analyze import analyze, authenticate
from .connection import is_connected_to_internet
from .highlight import highlight_errors, clear_previous_highlight
from .panels import show_results_in_panel
from .persist import DB
from .settings import get_token, get_concented, set_concented
from .statuses import set_status


def run_analysis(view):
    if not is_connected_to_internet():
        set_status(view, 'DeepCode: ❌ No Internet Connection  ')
        return

    if not view.window() or len(view.window().folders()) == 0:
        return

    project_path = view.window().folders()[0]

    if get_token() is None:
        authenticate(view)

    token = get_token()
    if token is None:
        return
    if project_path not in get_concented():
        set_status(view, 'DeepCode: Not activated for this project 🔐  ')
        concented = sublime.ok_cancel_dialog('Do you concent to DeepCode analyzing your project?', 'Yes')
        if not concented:
            return
        set_concented(project_path)

    set_status(view, 'DeepCode: Analyzing... ⏳ ')
    results = analyze(project_path, view)
    if results:
        DB[project_path] = results[0]
        sublime.set_timeout_async(lambda: show_results_in_panel(view, DB[project_path], results[1]))
        sublime.set_timeout_async(lambda: highlight_errors(view))


class DeepcodeAnalyzeCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.set_timeout_async(lambda: clear_previous_highlight(self.window.active_view()), 10)
        sublime.set_timeout_async(lambda: run_analysis(self.window.active_view()), 100)

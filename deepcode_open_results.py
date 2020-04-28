import webbrowser
import sublime
import sublime_plugin


class OpenUrlCommand(sublime_plugin.WindowCommand):
    def run(self, url):
        sublime.set_timeout_async(lambda: webbrowser.open_new_tab(url))

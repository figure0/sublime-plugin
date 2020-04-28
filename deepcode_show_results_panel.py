import sublime
import sublime_plugin

from .consts import PANEL_NAME


class DeepcodeShowResultsPanelCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command("show_panel", {"panel": "output.{}".format(PANEL_NAME)})

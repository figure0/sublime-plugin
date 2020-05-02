import sublime
import sublime_plugin


from .utils import find
from .highlight import highlight_errors, clear_previous_highlight
from .persist import HIGHLIGHTED_REGIONS
from .popup import get_popup_content


class DeepcodeHighlight(sublime_plugin.EventListener):
    def on_load(self, view):
        highlight_errors(view)

    def on_activated(self, view):
        highlight_errors(view)

    def on_hover(self, view, point, hover_zone):
        errors = HIGHLIGHTED_REGIONS.get(view.file_name())
        if errors is not None and len(errors) is not 0:
            popup_data = find(point, errors)
            if popup_data is not None:
                sublime.set_timeout_async(
                    lambda: view.show_popup(
                        get_popup_content(
                            popup_data.get("message"), popup_data.get("severity"), view
                        ),
                        sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        point,
                        1000,
                        1000,
                        lambda a: view.run_command(
                            "deep_code_ignore",
                            {"point": point, "type": a, "id": popup_data.get("id")},
                        ),
                    ),
                    300,
                )

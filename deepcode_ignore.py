import re

import sublime
import sublime_plugin
from Default.comment import build_comment_data

from .persist import HIGHLIGHTED_REGIONS


def get_ignore_text(type, id, append=False):
    ignoretext = "deepcode ignore" if type == "line" else "file deepcode ignore"
    if append:
        ignoretext = ", " + ignoretext
    return "{} {}: <please specify a reason of ignoring this> \n".format(ignoretext, id)


def does_comment_exist(line_text):
    return " deepcode ignore" in line_text


def update_highlighted_region(view, point, with_new_line=False):
    target = next(
        (
            error
            for error in HIGHLIGHTED_REGIONS[view.file_name()]
            if point in error["region"]
        ),
        None,
    )
    (x1, y1), (x2, y2) = (
        view.rowcol(target["region"][0]),
        view.rowcol(target["region"][-1]),
    )
    if with_new_line:
        x1 += 1
        x2 += 1
    else:
        # for some reason one character goes missing between comments
        y2 += 1

    def update_points():
        error_start_point, error_end_point = (
            view.text_point(x1, y1),
            view.text_point(x2, y2),
        )
        target["region"] = range(error_start_point, error_end_point)

    sublime.set_timeout(update_points, 500)


def insert_new_line_with_comment(view, edit, point, type, id, target):
    data = build_comment_data(view, target.begin())
    indent = re.findall(r"^\s*", view.substr(view.full_line(point)))[0]
    if data[0]:
        snip = "{0}{1}{2}".format(indent, data[0][0][0], get_ignore_text(type, id))
    elif data[1]:
        snip = "{0}{1} {2} {3}".format(
            indent, data[1][0][0], get_ignore_text(type, id), data[1][0][1]
        )
    else:
        return

    view.insert(edit, target.begin(), snip)
    view.sel().clear()
    view.sel().add(
        view.find(
            "<please specify a reason of ignoring this>",
            target.begin(),
            sublime.IGNORECASE,
        )
    )
    sublime.set_timeout_async(
        lambda: update_highlighted_region(view, point, with_new_line=True), 100
    )


def append_to_existing_comment(view, edit, point, type, id, target):
    (x, y) = view.rowcol(point)
    indent = re.findall(r"^\s*", view.substr(view.full_line(point)))[0]
    target_text = view.substr(target)
    snip = "{0}{1}{2}".format(
        indent, target_text.strip(), get_ignore_text(type, id, append=True)
    )
    update_highlighted_region(view, point)
    view.replace(edit, target, snip)
    view.sel().clear()
    view.sel().add(
        view.find(
            "<please specify a reason of ignoring this>",
            target.end(),
            sublime.IGNORECASE,
        )
    )
    target_updated = view.line(view.text_point(x - 1, y))
    sublime.set_timeout(lambda: view.show(target_updated.end()), 300)


class DeepCodeIgnoreCommand(sublime_plugin.TextCommand):
    def run(self, edit, point, type, id):
        if type == "panel":
            self.view.window().run_command("deepcode_show_results_panel")
        else:
            current_line = self.view.line(point)
            (x, y) = self.view.rowcol(point)
            previous_line = self.view.full_line(self.view.text_point(x - 1, y))
            previous_line_text = self.view.substr(previous_line)

            if does_comment_exist(previous_line_text):
                append_to_existing_comment(
                    self.view, edit, point, type, id, previous_line
                )
            else:
                insert_new_line_with_comment(
                    self.view, edit, point, type, id, current_line
                )

        # self.view.hide_popup()

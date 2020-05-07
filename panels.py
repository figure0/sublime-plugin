import os
import sublime

from .consts import PANEL_NAME, WARNING, ERROR, INFO
from .statuses import set_status
from .persist import HIGHLIGHTED_REGIONS
from .phantoms import (
    add_ingore_commands_phantom,
    add_see_results_phantom,
    remove_previous_phantoms,
)
from .utils import get_error_count, get_severity_status_string

phantom_counter = 0


def show_results_in_panel(view, resp, link):
    global phantom_counter
    project_folders = view.window().folders()
    if not project_folders:
        return

    panel = view.window().create_output_panel(PANEL_NAME)
    project_path = project_folders[0]

    configure_panel(panel, project_path)
    panel.set_read_only(False)
    remove_previous_phantoms(panel, phantom_counter)

    suggestions = resp.get("suggestions")

    numberOfIssues = 0
    numberOfFiles = 0
    problems = {
        WARNING: 0,
        ERROR: 0,
        INFO: 0,
    }

    files_with_issues = []

    for k, v in resp.get("files").items():
        numberOfFiles += 1
        file = get_formated_file_dict(project_path, k)
        for p, pv in v.items():
            for error in pv:
                severity = suggestions.get(p).get("severity")
                problems[severity] += 1
                file["total"][severity] += 1
                file["issues"].append(
                    get_formated_file_issue(severity, file, error, p, suggestions)
                )
                numberOfIssues += 1
        files_with_issues.append(file)

    ISSUES_TEXT_BASE = "Deepcode: Found problems: {} in {} file(s) ".format(
        numberOfIssues, numberOfFiles
    )
    report_message = get_error_count(problems, ISSUES_TEXT_BASE)

    print_results(panel, files_with_issues, report_message, phantom_counter)
    add_see_results_phantom(panel, link)

    panel.set_read_only(True)

    if numberOfIssues > 0:
        sublime.set_timeout(lambda: set_status(view, report_message), 100)
    else:
        sublime.set_timeout(
            lambda: set_status(view, "DeepCode: No errors found ✅"), 100
        )


def configure_panel(panel, project_path):
    panel.settings().set("gutter", True)
    panel.settings().set("color_scheme", "Mariana.sublime-color-scheme")
    panel.settings().set(
        "result_file_regex", r"(?:⚠️|⛔|ⓘ) (.*) \[(\d+), (\d+)\]: (.*) "
    )
    panel.settings().set("line_numbers", False)
    panel.settings().set("line_padding_bottom", 5)
    panel.settings().set("line_padding_top", 15)
    panel.settings().set("result_base_dir", project_path)


def get_formated_file_dict(project_path, file_name):
    return {
        "name": file_name.replace(project_path + "/", ""),
        "original_name": file_name,
        "total": {WARNING: 0, ERROR: 0, INFO: 0},
        "issues": [],
    }


def get_formated_file_issue(severity, file, error, suggestion_index, suggestions):
    return {
        "severity": severity,
        "message": "  {} {} [{}, {}]: {}".format(
            get_severity_status_string(severity),
            file["name"],
            error.get("rows")[0],
            error.get("cols")[0],
            suggestions.get(suggestion_index).get("message"),
        ),
        "row": error.get("rows")[0],
        "col": error.get("cols")[0],
        "reason": suggestions.get(suggestion_index).get("rule"),
    }


def print_results(panel, files_with_issues, report_message, phantom_counter):
    panel.run_command("append", {"characters": "{}    ".format(report_message)})
    panel.run_command("append", {"characters": "› \n"})

    files_with_issues.sort(
        key=lambda k: (k["total"][ERROR], k["total"][WARNING], k["total"][INFO]),
        reverse=True,
    )
    for record in files_with_issues:
        record["issues"] = sorted(
            record["issues"], key=lambda k: k["severity"], reverse=True
        )

    for file in files_with_issues:
        panel.run_command(
            "append",
            {
                "characters": "{} \n".format(
                    get_error_count(file["total"], "{} ".format(file["name"]))
                )
            },
        )
        for index, issue in enumerate(file["issues"]):
            panel.run_command("append", {"characters": "{}\n".format(issue["message"])})
            if len(file["issues"]) - 1 == index:
                panel.run_command("append", {"characters": "{}\n".format("     ⠀")})
            phantom_counter += 1
            add_ingore_commands_phantom(
                panel, phantom_counter, file["original_name"], issue
            )
    panel.run_command("fold_all")

import re

from .consts import STATUS_KEY, MAIN_STATUSES, SUB_STATUSES
from .statuses import set_status

MSG = "([A-Za-z\\s]+).*\\d+(?:%|f\\s\\[)"
MSG_FROM_PREV_STATUS = "DeepCode - (.*%)\s"
PERCENT = "(\d+)%"
FILE_COUNT = "(\d+)f \\["
CLI_ERROR = "deepcode\s+:\s+ERROR\s+(.*)"
SERVER_UNAVAILABLE = "deepcode\s+:\s+WARNING\s+(.*)"

common_wrap = lambda msg: "DeepCode - {} ⏳".format(msg)


def get_by_regex(regex, line):
    return next((x for x in re.findall(r"{}".format(regex), line)), None)


def get_main_status_order(msg):
    try:
        return MAIN_STATUSES.index(msg)
    except ValueError:
        return -1


def get_prev_msg(prev_status):
    return next(
        (x for x in re.findall(r"{}".format(MSG_FROM_PREV_STATUS), prev_status)), None
    )


def is_sub_status(msg):
    try:
        SUB_STATUSES.index(msg)
        return True
    except ValueError:
        return False


def handle_main_status(msg, order, sub_progress=0):
    try:
        if order == 0:
            return "{}...".format(msg)
        return "{} {}%".format(msg, order * 20 + sub_progress)
    except ValueError:
        print("Unrecognized progress status received")


def get_progress_status(line, prev_status):
    msg = get_by_regex(MSG, line)
    if msg is None:
        return msg
    main_status_order = get_main_status_order(msg)
    if main_status_order > 0:
        return common_wrap(handle_main_status(msg, main_status_order))
    if is_sub_status(msg):
        prev_msg = get_prev_msg(prev_status)
        percentage = get_by_regex(PERCENT, line)
        if percentage is not None:
            parent_msg = get_by_regex(MSG, prev_msg)
            if parent_msg is not None:
                parent_status_order = get_main_status_order(parent_msg.strip())
                parent_status_updated_msg = handle_main_status(
                    parent_msg.strip(),
                    parent_status_order,
                    sub_progress=int(int(percentage) / 5),
                )
                return common_wrap(
                    "{} ({} {}%)".format(parent_status_updated_msg, msg, percentage)
                )
        file_count = get_by_regex(FILE_COUNT, line)
        if file_count is not None:
            return common_wrap("{} ({}: {})".format(prev_msg, msg, file_count))


def is_auth_error(line):
    return get_by_regex(CLI_ERROR, line)


def is_server_unavailable(line):
    return get_by_regex(SERVER_UNAVAILABLE, line)


def handle_progress_update(progress_data, view):
    for line in progress_data:
        if len(line.strip()) > 0:
            if is_auth_error(line):
                raise Exception("Unauthorized")
            if is_server_unavailable(line):
                raise Exception("Server Unavailable")
            status = get_progress_status(line, view.get_status(STATUS_KEY))
            if status:
                view.set_status(STATUS_KEY, status)
                continue
            if "Completed analysis" in line:
                # This makes no sense, but for some reason is necessary for large repos
                break

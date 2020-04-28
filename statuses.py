from .consts import STATUS_KEY


def set_status(view, status):
    view.set_status(STATUS_KEY, status)

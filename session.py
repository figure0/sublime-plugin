SESSION_STORAGE = {"python_version_valid": False, "asked_to_consent": []}


def is_python_version_valid():
    return SESSION_STORAGE.get("python_version_valid")


def set_is_python_version_valid(is_valid):
    SESSION_STORAGE["python_version_valid"] = is_valid


def user_asked_to_consent_for_project(project_path):
    return project_path in SESSION_STORAGE["asked_to_consent"]


def add_project_to_asked_to_consent(project_path):
    if user_asked_to_consent_for_project(project_path):
        return

    SESSION_STORAGE["asked_to_consent"].append(project_path)

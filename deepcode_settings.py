import sublime, sublime_plugin, json
from .settings import get_settings
from .consts import (
    DEEP_CODE_SETTINGS_DEBUG_KEY,
    DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY,
    DEEP_CODE_SETTINGS_CONSENT_KEY,
    DEEP_CODE_SETTINGS_SERVICE_URL_KEY,
    DEEP_CODE_SETTINGS_TOKEN_KEY,
    DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH,
)
from .phantoms import add_settings_key_description_phantom

USER_SETTING = "User"
SETTINGS_FILE_NAME = "DeepcodeAI.sublime-settings"
HIGHLIGHT_REGION_NAME = "settings_errors"


class DeepcodeSettings(sublime_plugin.EventListener):
    def on_load(self, view):
        filename = view.file_name().split("/")
        file = filename[-1]
        level = filename[-2]
        if file == SETTINGS_FILE_NAME and level != USER_SETTING:
            view.set_read_only(True)
            add_settings_key_description_phantom(
                view,
                DEEP_CODE_SETTINGS_TOKEN_KEY,
                "Authentication token as a result of login.",
            )
            add_settings_key_description_phantom(
                view,
                DEEP_CODE_SETTINGS_SERVICE_URL_KEY,
                "Custom DeepCode service URL (default:https://www.deepcode.ai).",
            )
            add_settings_key_description_phantom(
                view,
                DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY,
                "Enables liters analyses, along DeepCode analyses.",
            )
            add_settings_key_description_phantom(
                view, DEEP_CODE_SETTINGS_DEBUG_KEY, "Forward all debugging messages."
            )
            add_settings_key_description_phantom(
                view,
                DEEP_CODE_SETTINGS_CONSENT_KEY,
                "List of projects, that you have consented for DeepCode to analyze.",
            )
            add_settings_key_description_phantom(
                view,
                DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH,
                "Change in case python 3 is installed somewhere atypically on your system.",
            )

    def on_pre_save(self, view):
        filename = view.file_name().split("/")
        file = filename[-1]
        level = filename[-2]
        errors = []
        if file == SETTINGS_FILE_NAME and level == USER_SETTING:
            try:
                new_settings = json.loads(view.substr(sublime.Region(0, view.size())))

                if DEEP_CODE_SETTINGS_TOKEN_KEY in new_settings and not isinstance(
                    new_settings.get(DEEP_CODE_SETTINGS_TOKEN_KEY), str
                ):
                    sublime.error_message(
                        "⛔ Settings key {} is invalid, {} must be string.".format(
                            DEEP_CODE_SETTINGS_TOKEN_KEY, DEEP_CODE_SETTINGS_TOKEN_KEY
                        )
                    )
                    errors.append(
                        view.find(DEEP_CODE_SETTINGS_TOKEN_KEY, 0, sublime.IGNORECASE)
                    )

                if (
                    DEEP_CODE_SETTINGS_SERVICE_URL_KEY in new_settings
                    and not isinstance(
                        new_settings.get(DEEP_CODE_SETTINGS_SERVICE_URL_KEY), str
                    )
                ):
                    sublime.error_message(
                        "⛔ Settings key {} is invalid, {} must be string.".format(
                            DEEP_CODE_SETTINGS_SERVICE_URL_KEY,
                            DEEP_CODE_SETTINGS_SERVICE_URL_KEY,
                        )
                    )
                    errors.append(
                        view.find(
                            DEEP_CODE_SETTINGS_SERVICE_URL_KEY, 0, sublime.IGNORECASE
                        )
                    )

                if (
                    DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY in new_settings
                    and not isinstance(
                        new_settings.get(DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY), bool
                    )
                ):
                    sublime.error_message(
                        "⛔ Settings key {} is invalid, {} must be boolean.".format(
                            DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY,
                            DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY,
                        )
                    )
                    errors.append(
                        view.find(
                            DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY, 0, sublime.IGNORECASE
                        )
                    )

                if DEEP_CODE_SETTINGS_DEBUG_KEY in new_settings and not isinstance(
                    new_settings.get(DEEP_CODE_SETTINGS_DEBUG_KEY), bool
                ):
                    sublime.error_message(
                        "⛔ Settings key {} is invalid, {} must be boolean.".format(
                            DEEP_CODE_SETTINGS_DEBUG_KEY, DEEP_CODE_SETTINGS_DEBUG_KEY
                        )
                    )
                    errors.append(
                        view.find(DEEP_CODE_SETTINGS_DEBUG_KEY, 0, sublime.IGNORECASE)
                    )

                if DEEP_CODE_SETTINGS_CONSENT_KEY in new_settings and not isinstance(
                    new_settings.get(DEEP_CODE_SETTINGS_CONSENT_KEY), list
                ):
                    sublime.error_message(
                        "⛔ Settings key {} is invalid, {} must be an array of project paths.".format(
                            DEEP_CODE_SETTINGS_CONSENT_KEY,
                            DEEP_CODE_SETTINGS_CONSENT_KEY,
                        )
                    )
                    errors.append(
                        view.find(DEEP_CODE_SETTINGS_CONSENT_KEY, 0, sublime.IGNORECASE)
                    )

                if (
                    DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH in new_settings
                    and not isinstance(
                        new_settings.get(DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH), str
                    )
                ):
                    sublime.error_message(
                        "⛔ Settings key {} is invalid, {} must be string.".format(
                            DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH,
                            DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH,
                        )
                    )
                    errors.append(
                        view.find(
                            DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH, 0, sublime.IGNORECASE
                        )
                    )

                view.add_regions(
                    HIGHLIGHT_REGION_NAME,
                    list(map(view.word, errors)),
                    "region.redish.plugin",
                    "",
                    sublime.DRAW_SQUIGGLY_UNDERLINE | sublime.DRAW_NO_OUTLINE,
                )
            except Exception as e:
                revert = sublime.error_message(
                    "⛔ Settings are not valid. Settings file must be in valid JSON format"
                )

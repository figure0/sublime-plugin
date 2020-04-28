import sublime
import json
import os

from .consts import DEEP_CODE_SETTINGS_CONSENT_KEY, DEEP_CODE_SETTINGS_TOKEN_KEY, DEEP_CODE_SETTINGS_SERVICE_URL_KEY, DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY, DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH


def set_initial_settings_if_needed(): 
    deepcode_settings = sublime.load_settings('Deepcode.sublime-settings')
    if deepcode_settings is None:
        sublime.load_settings('Deepcode.sublime-settings')        
        sublime.save_settings("Deepcode.sublime-settings")

def get_settings():
    return sublime.load_settings('Deepcode.sublime-settings')

def set_settings(path, value):
    settings = sublime.load_settings('Deepcode.sublime-settings')
    sublime.load_settings('Deepcode.sublime-settings').set(path, value)
    sublime.save_settings("Deepcode.sublime-settings")

def get_token():
    deepcode_settings = get_settings()
    return deepcode_settings.get(DEEP_CODE_SETTINGS_TOKEN_KEY)

def set_token(token):
    set_settings(DEEP_CODE_SETTINGS_TOKEN_KEY, token)

def get_consented():
    deepcode_settings = get_settings()
    return deepcode_settings.get(DEEP_CODE_SETTINGS_CONSENT_KEY, [])

def set_consented(project_path):
    deepcode_settings = get_settings()
    consented = deepcode_settings.get(DEEP_CODE_SETTINGS_CONSENT_KEY, [])
    consented.append(project_path)
    set_settings(DEEP_CODE_SETTINGS_CONSENT_KEY, consented)

def get_service_url():
    settings = get_settings()
    return settings.get(DEEP_CODE_SETTINGS_SERVICE_URL_KEY, '')

def get_linters_enabled():
    settings = get_settings()
    return settings.get(DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY, '')

def get_custom_python_path():
    settings = get_settings()
    return settings.get(DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH, None)

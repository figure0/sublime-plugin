ERROR = 1
WARNING = 2
INFO = 3

AUTH_TIMEOUT = 30

PANEL_NAME = 'deepcode'
HIGHLIGH_REGION_NAME = 'deepcode_highlight'
STATUS_KEY = 'deepcode_status'
PANEL_IGNORE_PHANTOM_BASE_NAME='deepcode_panel_ignore'

DEEP_CODE_STTINGS_TOKEN_KEY = 'token'
DEEP_CODE_SETTING_CONSENT_KEY = 'concented'
DEEP_CODE_SETTING_SERVICE_URL_KEY = 'serviceUrl'
DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY = 'enableLinters'
DEEP_CODE_SETTINGS_DEBUG_KEY = 'debug'

MAIN_STATUSES = [
    'Fetching supported extensions',
    'Scanning for files',
    'Computing file hashes',
    'Sending data',
    'Requesting audit results'
]

SUB_STATUSES = [
    'Found files',
    'Calculated hashes',
    'Generated bundles'
]


ERROR = 1
WARNING = 2
INFO = 3

AUTH_TIMEOUT = 60

PANEL_NAME = 'deepcode'
HIGHLIGH_REGION_NAME = 'deepcode_highlight'
STATUS_KEY = 'deepcode_status'
PANEL_IGNORE_PHANTOM_BASE_NAME='deepcode_panel_ignore'

DEEP_CODE_SETTINGS_TOKEN_KEY = 'token'
DEEP_CODE_SETTINGS_CONSENT_KEY = 'consented'
DEEP_CODE_SETTINGS_SERVICE_URL_KEY = 'serviceUrl'
DEEP_CODE_SETTINGS_ENABLE_LINTERS_KEY = 'enableLinters'
DEEP_CODE_SETTINGS_DEBUG_KEY = 'debug'
DEEP_CODE_SETTINGS_CUSTOM_PYTHON_PATH = 'customPythonPath'

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

MAC_OS_BIN_PATHS = ['/bin', '/usr/bin', '/usr/sbin', '/usr/local/bin', '/sbin', '/usr/X11/bin']


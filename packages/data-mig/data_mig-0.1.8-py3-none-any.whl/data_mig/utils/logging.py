import requests
import traceback
from types import TracebackType
from enum import Enum
import sys

class LogEntryTypes(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    INFO = 'INFO'


def strip_bcolors(st: str):
    import inspect
    for i in inspect.getmembers(bcolors):
        if not i[0].startswith('_'):
            st = st.replace(i[1], '')
    return st


class Logging(object):
    def __init__(self, config):
        self._config = config.NOTIFICATIONS
        self._active_profile = config.NOTIFICATIONS.get('active_profile')
        self._profiles = config.NOTIFICATIONS.get('profiles')
        self._debug = config.NOTIFICATIONS.get('debug', False)

    def log(self, message, type: LogEntryTypes = LogEntryTypes.INFO):
        notify_on_types = self._config.get('notify_on')
        c = getattr(bcolors, type.value)
        try:
            if isinstance(message, (Exception, TracebackType)):
                exc_type, value, tb = sys.exc_info()
                message = f"{c}{type.value}: {value}{bcolors.ENDC}"
                if isinstance(tb, TracebackType) and self._debug:
                    traceback.print_tb(tb)
            else:
                message = f"{c}{type.value}: {message}{bcolors.ENDC}"
            print(message)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            print(f"{bcolors.ERROR}ERROR: Exception in logging error: {exc_type} {value}{bcolors.ENDC}")

        if self._profiles.get('slack') and notify_on_types and type.value in notify_on_types:
            profiles = self._profiles.get('slack')
            url = profiles.get('webhook_url')
            data = {'text': strip_bcolors(message)}
            requests.post(url, json=data)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ERROR = FAIL
    SUCCESS = OKBLUE
    INFO = OKCYAN
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



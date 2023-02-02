from datetime import datetime
from inspect import getframeinfo, stack

WHITE: str = '\x1b[38;20m'
GREY: str = '\x1b[38;20m'
DARK_GREY: str = '\x1b[30;20m'
YELLOW: str = '\x1b[33;20m'
RED: str = '\x1b[31;20m'
BOLD_RED: str = '\x1b[31;1m'
RESET: str = '\x1b[0m'

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4


class Level:
    def __init__(self, id: int, name: str, color: str):
        self.id: int = id
        self.name: str = name
        self.color: str = color


levels = {
    DEBUG: Level(DEBUG, 'DEBUG', GREY),
    INFO: Level(INFO, 'INFO', WHITE),
    WARNING: Level(WARNING, 'WARNING', YELLOW),
    ERROR: Level(ERROR, 'ERROR', RED),
    CRITICAL: Level(CRITICAL, 'CRITICAL', BOLD_RED),
}


class Logger:
    def __init__(self, name: str, level: int = INFO):
        self.name: str = name
        self.base_level: Level = levels[level]

    def get_formated_message(self, message: str, level: Level) -> str:
        now: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        caller = getframeinfo(stack()[2][0])
        filename = 'src/' + caller.filename.replace('\\', '/').split('/src/', 1)[1]
        return f'{level.color} {now} ({level.name}): {message} {DARK_GREY}({filename}:{caller.lineno}) {RESET}'

    def debug(self, message):
        if DEBUG >= self.base_level.id:
            msg = self.get_formated_message(message, levels[DEBUG])
            print(msg)

    def info(self, message):
        if INFO >= self.base_level.id:
            msg = self.get_formated_message(message, levels[INFO])
            print(msg)

    def warning(self, message):
        if WARNING >= self.base_level.id:
            msg = self.get_formated_message(message, levels[WARNING])
            print(msg)

    def error(self, message):
        if ERROR >= self.base_level.id:
            msg = self.get_formated_message(message, levels[ERROR])
            print(msg)

    def critical(self, message):
        if CRITICAL >= self.base_level.id:
            msg = self.get_formated_message(message, levels[CRITICAL])
            print(msg)

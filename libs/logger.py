import logging
from enum import Enum


class _ANSICode(Enum):
    DEBUG = "\x1b[37m"
    INFO = "\x1b[37m"
    WARNING = "\x1b[33m"
    ERROR = "\x1b[31m"
    CRITICAL = "\x1b[31m"
    RESET = "\x1b[0m"


class _Formatter(logging.Formatter):
    FORMAT = "[%(levelname)s] [%(name)s] %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        color = _ANSICode[record.levelname].value
        reset = _ANSICode.RESET.value
        string = f"{color}{self.FORMAT}{reset}"
        formatter = logging.Formatter(string)
        return formatter.format(record)


def get_log(name: str) -> logging.Logger:
    stream = logging.StreamHandler()
    stream.setFormatter(_Formatter())
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(stream)
    return log

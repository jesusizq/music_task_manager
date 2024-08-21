from enum import Enum
from datetime import datetime


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Logger:
    def __init__(self, level=LogLevel.INFO):
        self.level = level

    def log(self, level: LogLevel, message: str):
        """Logs a message if the level is greater than or equal to the Logger's level."""
        if self.level.value <= level.value:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] [{level.name}] {message}")

    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)

    def error(self, message: str):
        self.log(LogLevel.ERROR, message)

    def critical(self, message: str):
        self.log(LogLevel.CRITICAL, message)

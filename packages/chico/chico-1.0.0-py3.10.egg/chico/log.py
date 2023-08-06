#!/usr/bin/env python3

import logging


class Logger(logging.Logger):
    def __init__(
        self, logname=None, filename=None, level=logging.DEBUG, overwirte=False
    ):
        super().__init__(name=logname, level=level)
        self.empty_handlers()
        self.formatter = get_formatter()
        self.console_log = logging.StreamHandler()
        self.set_console()
        self.file_log = None
        self.set_logfile(filename, overwirte)

    def set_console(self):
        self.console_log.setLevel(self.level)
        self.console_log.setFormatter(self.formatter)
        self.addHandler(self.console_log)

    def set_logfile(self, filename=None, overwirte=False):
        if filename is not None:
            self.file_log = logging.FileHandler(
                filename=filename, mode="w" if overwirte else "a"
            )
            self.file_log.setFormatter(logging.DEBUG)
            self.file_log.setFormatter(self.formatter)
            self.addHandler(self.file_log)

    def set_formatter(self, fmt, datefmt):
        self.formatter = logging.Formatter(fmt, datefmt)

    def empty_handlers(self):
        while self.hasHandlers():
            self.removeHandler(self.handlers[0])


def get_formatter():
    return logging.Formatter(
        "[%(asctime)s] %(name)s: %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

import logging
from copy import copy

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'DEBUG': 30 + BLUE,
    'INFO': 30 + GREEN,
    'WARNING': 30 + YELLOW,
    'HTTP': 30 + CYAN,
    'ERROR': 30 + RED,
}

PREFIX = '\033['
SUFFIX = '\033[0m'

TIME = '%Y-%m-%d %H:%M:%S'
FORMAT = "%(asctime)s | [%(levelname)-7s] | %(message)s %(status)s %(data)s"


class LoggerFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        try:
            _record = copy(record)
            status: int | None = record.args.get("status") if record.args else None
            data: dict[str, any] | None = record.args.get("data") if record.args else None

            if status and type(status) != int: raise TypeError('Status type must be integer.')

            _record.status = f'| [STATUSCODE {status}]' if status else ""
            _record.data = f'| {data}' if data else ""

            message = logging.Formatter.format(self, _record)
            color = COLORS.get(_record.levelname.upper(), 37)

            return '{0}{1}m{2}{3}'.format(PREFIX, color, message, SUFFIX)
        except Exception as error:
            return f"Error while logging your message: {error}"


def setup_logger(appname: str):
    HTTP = logging.DEBUG + 2
    logging.addLevelName(HTTP, "HTTP")

    # Silence other loggers
    for log_name, log_obj in logging.Logger.manager.loggerDict.items():
        if log_name != appname:
            log_obj.disabled = True

    def http(self, message, *args, **kws):
        self.log(HTTP, message, *args, **kws)

    logging.Logger.http = http

    logger = logging.getLogger(appname)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(LoggerFormatter(FORMAT, TIME))

    logger.addHandler(ch)
    return logger


class PyLogger:
    def __init__(self, appname: str = "myapp"):
        self.logger = setup_logger(appname)

    @staticmethod
    def check_params(status_code, data):
        obj = {}
        if status_code: obj.update({"status": status_code})
        if data: obj.update({"data": data})
        return obj

    def error(self, message: str, status_code: int = None, data=None):
        args = self.check_params(status_code, data)
        if args:
            self.logger.error(message, args)
        else:
            self.logger.error(message)

    def warning(self, message: str, status_code: int = None, data=None):
        args = self.check_params(status_code, data)
        if args:
            self.logger.warning(message, args)
        else:
            self.logger.warning(message)

    def debug(self, message: str, status_code: int = None, data=None):
        args = self.check_params(status_code, data)
        if args:
            self.logger.debug(message, args)
        else:
            self.logger.debug(message)

    def info(self, message: str, status_code: int = None, data=None):
        args = self.check_params(status_code, data)
        if args:
            self.logger.info(message, args)
        else:
            self.logger.info(message)

    def http(self, message: str, status_code: int = None, data=None):
        args = self.check_params(status_code, data)
        if args:
            self.logger.http(message, args)
        else:
            self.logger.http(message)

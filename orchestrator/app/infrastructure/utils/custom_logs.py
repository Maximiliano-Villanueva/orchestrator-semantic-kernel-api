import logging


class LogColors:
    RED = "\033[91m"
    YELLOW = "\033[93m"
    ORANGE = "\033[38;5;208m" 
    CYAN = "\033[36m"
    RESET = "\033[0m"


class CustomFormatter(logging.Formatter):
    COLOR_MAP = {
        logging.ERROR: LogColors.RED,
        logging.WARNING: LogColors.YELLOW,
        logging.INFO: LogColors.CYAN,
    }

    def format(self, record):
        color = self.COLOR_MAP.get(record.levelno)
        if color:
            record.msg = f"{color}{record.msg}{LogColors.RESET}"
        return super().format(record)


def getLogger(name, level=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO if not level else level)

    log_format = "%(asctime)s - %(pathname)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s"
    formatter = CustomFormatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger



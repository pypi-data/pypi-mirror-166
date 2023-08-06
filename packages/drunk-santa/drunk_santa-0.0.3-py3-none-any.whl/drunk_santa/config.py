import os
from logging.config import dictConfig

if os.getenv("BASE_URL"):  # pana la beers
    BASE_URL = os.getenv("BASE_URL")
else:
    BASE_URL = "https://api.punkapi.com/v2/beers"

TOTAL_RETRIES = 5
BACKOFF_FACTOR = 10
STATUS_FORCELIST = [502, 503, 504]


logging_schema = {
    "version": 1,
    "formatters": {
        "standard": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(message)s - %(funcName)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": "log_history.log",
            "maxBytes": 500000,
            "backupCount": 1,
        },
    },
    "loggers": {
        "__name__": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {"level": "INFO", "handlers": ["file"]},
}

dictConfig(logging_schema)

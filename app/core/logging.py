import logging
import logging.config

DEFAULT_LOG_LEVEL = "INFO"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        # Your app loggers
        "app": {"handlers": ["console"], "level": DEFAULT_LOG_LEVEL, "propagate": False},
        # Make uvicorn/uvicorn.access play nicely with the same handler/format
        "uvicorn": {"handlers": ["console"], "level": DEFAULT_LOG_LEVEL, "propagate": False},
        "uvicorn.error": {"handlers": ["console"], "level": DEFAULT_LOG_LEVEL, "propagate": False},
        "uvicorn.access": {"handlers": ["console"], "level": DEFAULT_LOG_LEVEL, "propagate": False},
    },
    "root": {  # fallback
        "handlers": ["console"],
        "level": DEFAULT_LOG_LEVEL,
    },
}

def setup_logging(level: str | None = None) -> None:
    if level:
        LOGGING_CONFIG["loggers"]["app"]["level"] = level
        LOGGING_CONFIG["root"]["level"] = level
        LOGGING_CONFIG["loggers"]["uvicorn"]["level"] = level
        LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] = level
        LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] = level
    logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

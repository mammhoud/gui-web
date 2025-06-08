import os
import structlog
from colorlog import ColoredFormatter


def inject_contexts(_, __, event_dict):
    from django.utils.timezone import now

    event_dict["timestamp"] = now().isoformat()  # Add timestamp

    # Remove empty fields to avoid cluttering logs
    event_dict = {k: v for k, v in event_dict.items() if v is not None}
    return event_dict


# Colored Flatline Formatter
class ColoredFlatlineFormatter(ColoredFormatter):
    def __init__(self):
        super().__init__(
            "%(log_color)s[%(name)s:%(lineno)d:%(levelname)s] -  %(log_color)s%(message)s",
            log_colors={
                "DEBUG": "white",
                "INFO": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            secondary_log_colors={},
            style="%",
        )


# Logging Configurations
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored_flatline": {
            "()": ColoredFlatlineFormatter,
        },
        "colored_console": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(asctime)s] - [%(levelname)s] - [%(name)s:%(lineno)d] - %(message)s",
        },
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso", utc=False),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
            ],
        },
        "key_value_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"],
                drop_missing=True,
            ),
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored_console",
            "level": "DEBUG",
        },
        "flat": {
            "class": "logging.StreamHandler",
            "formatter": "colored_flatline",
            "level": "DEBUG",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Structlog Configuration
structlog.configure(
    processors=[
        inject_contexts,  # Inject dynamic context fields
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

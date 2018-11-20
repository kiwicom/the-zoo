"""Configuration of ``structlog``."""
import structlog


def float_rounder(_, __, event_dict):
    """Round any floats in ``event_dict`` to 3 decimal places."""
    for (key, value) in list(event_dict.items()):
        if isinstance(value, float):
            event_dict[key] = round(value, 3)
    return event_dict


def drop_debug_logs(_, __, event_dict):
    """Drop event with ``debug`` log level."""
    if event_dict["level"] == "debug":
        raise structlog.DropEvent

    return event_dict


PRODUCTION_PROCESSORS = [
    structlog.stdlib.add_log_level,
    drop_debug_logs,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(),
    float_rounder,
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    structlog.processors.JSONRenderer(),
]

DEBUG_PROCESSORS = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper("iso"),
    float_rounder,
    structlog.processors.ExceptionPrettyPrinter(),
    structlog.processors.UnicodeDecoder(),
    structlog.dev.ConsoleRenderer(pad_event=25),
]


def configure_structlog(debug: bool):
    """Configure proper log processors and settings for structlog with regards to debug setting."""
    processors = DEBUG_PROCESSORS if debug else PRODUCTION_PROCESSORS

    structlog.configure_once(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=structlog.threadlocal.wrap_dict(dict),
    )

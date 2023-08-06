"""A module with pre-chewed logging helpers.

"""
import logging
import os
from datetime import datetime


def get_file_logger(
    logger_name: str,
    log_level=logging.INFO,
    log_file_directory=".",
    log_format="%(asctime)s %(name)-30s %(levelname)-8s %(message)s",
) -> logging.Logger:
    """Create a basic logger with a standardised file handler.

    Creates a logger instance with a file handler.
    Logs will be sent to standard output and to a file. The file will have the date and time in its name.
    Each time this is run (up to once per second), a new logger is created with a new file name.

    By default, the log file is created in the working directory.

    Args:
        logger_name: The name of the logger (std logging recommends you use `__main__`)
        log_level: The log level (default is `logging.INFO`)
        log_file_directory: The directory the logfile should be created in.
        log_format: The log format to use. The default is "%(asctime)s %(name)-30s %(levelname)-8s %(message)s".

    Returns:
        A logging instance with an attached file handler.

    """
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(logger_name)

    datetime_str = datetime.now().isoformat().replace(":", "-")
    log_file = os.path.join(log_file_directory, f"runlogs.{datetime_str}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(
        logging.Formatter(log_format),
    )

    logger.addHandler(file_handler)
    return logger

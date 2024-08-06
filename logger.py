import logging
import sys

def setup_logging(app):
    """
    Set up logging configuration using the app's configuration for log level.
    Logs are written only to the console.
    """

    # Get the log level from the app configuration
    log_level = app.config.get('LOG_LEVEL', 'DEBUG').upper()

    # Create a logger object and set the level
    logger = app.logger
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create and add a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level, logging.DEBUG))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Log the setup details
    logger.info(f"Logging is set up. Level: {log_level}")

    return logger

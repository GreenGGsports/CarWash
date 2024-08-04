import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """
    Set up logging configuration using the app's configuration for log level.
    The logs are written to 'app.log' file with a rotating file handler.
    """

    # Get the log level from the app configuration
    log_level = app.config.get('LOG_LEVEL', 'DEBUG').upper()

    # Create a logger object and set the level
    logger = app.logger
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))

    # Create a file handler for logging
    file_handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    
    # Set the log level for the file handler
    file_handler.setLevel(getattr(logging, log_level, logging.DEBUG))

    # Create a log formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    # Optionally add a console handler for debugging purposes
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level, logging.DEBUG))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Log the setup details
    logger.info(f"Logging is set up. Level: {log_level}, Log file: app.log")

    return logger

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# configs/logging_config.py
DEBUG = True
SECRET_KEY = 'your_secret_key'


def setup_logging():
    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set up a basic configuration for logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # Get the current date and time formatted as YYYY-MM-DD-HH
    current_datetime = datetime.now().strftime('%Y-%m-%d-%H')

    # Create a log file name with the current date and time
    log_file_name = f'logs/{current_datetime}.log'

    # Initialize the RotatingFileHandler
    file_handler = RotatingFileHandler(
        filename=log_file_name,
        maxBytes=10240,
        backupCount=10
    )

    # Set the formatter for the handler
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    # Set the log level for the handler
    file_handler.setLevel(logging.INFO)
    # Add the file handler to the root logger
    logging.getLogger().addHandler(file_handler)

    # Log that logging is set up
    logging.getLogger().info('Logging setup complete')

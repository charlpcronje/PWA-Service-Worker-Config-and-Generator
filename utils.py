# utils.py

import logging
from colorama import Fore

def setup_logging() -> logging.Logger:
    """
    Set up logging to both file and console.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger('service_worker_app')
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler('service_worker_app.log')
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    print(f"{Fore.GREEN}Logging setup complete{Fore.RESET}")
    return logger

# Add any other utility functions here
# file_analyzer.py

from pathlib import Path
from typing import Dict, Any, List
import logging
from colorama import Fore

class FileAnalyzer:
    """
    Class for analyzing the file structure based on the configuration.

    Attributes:
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize the FileAnalyzer.

        Args:
            logger (logging.Logger): Logger instance.
        """
        self.logger = logger

    def analyze(self, config: Dict[str, Any]) -> List[str]:
        """
        Analyze the file structure based on the configuration.

        Args:
            config (Dict[str, Any]): The service worker configuration.

        Returns:
            List[str]: List of files to be included in the service worker.
        """
        root_path = Path(config['root_path'])
        included_files = []

        for pattern in config['include']:
            for file_path in root_path.glob(pattern):
                if file_path.is_file():
                    relative_path = file_path.relative_to(root_path)
                    included_files.append(str(relative_path))
                    self.logger.info(f"Including file: {relative_path}")

        self.logger.info(f"Total files included: {len(included_files)}")
        print(f"{Fore.GREEN}Total files included: {len(included_files)}{Fore.RESET}")
        return included_files
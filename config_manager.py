# config_manager.py

import json
import os
from typing import Dict, Any, List
import logging
from pathlib import Path
from colorama import Fore

class ConfigManager:
    """
    Class for managing service worker configuration.

    Attributes:
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize the ConfigManager.

        Args:
            logger (logging.Logger): Logger instance.
        """
        self.logger = logger

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a JSON file.

        Args:
            config_path (str): Path to the JSON configuration file.

        Returns:
            Dict[str, Any]: The loaded configuration.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            json.JSONDecodeError: If the configuration file is not valid JSON.
        """
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {config_path}")
            print(f"{Fore.GREEN}Configuration loaded from {config_path}{Fore.RESET}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            print(f"{Fore.RED}Configuration file not found: {config_path}{Fore.RESET}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in configuration file: {config_path}")
            print(f"{Fore.RED}Invalid JSON in configuration file: {config_path}{Fore.RESET}")
            raise

    def generate_config(self, root_path: str) -> Dict[str, Any]:
        """
        Generate configuration interactively.

        Args:
            root_path (str): Root path of the web application.

        Returns:
            Dict[str, Any]: The generated configuration.
        """
        config = {
            "root_path": root_path,
            "include": [],
            "exclude": [],
            "cache_on_install": [],
            "cache_on_demand": []
        }

        self._explore_directory(Path(root_path), config)

        self.logger.info("Configuration generated interactively")
        print(f"{Fore.GREEN}Configuration generated interactively{Fore.RESET}")
        return config

    def _explore_directory(self, path: Path, config: Dict[str, Any]) -> None:
        """
        Recursively explore a directory and update the configuration.

        Args:
            path (Path): Path to explore.
            config (Dict[str, Any]): Configuration to update.
        """
        try:
            items = sorted(path.iterdir())
            selected = self._select_items(items, path)

            for item in selected:
                relative_path = item.relative_to(config['root_path'])
                if item.is_dir():
                    config['include'].append(str(relative_path / '*'))
                    self._explore_directory(item, config)
                else:
                    config['include'].append(str(relative_path))
        except PermissionError:
            self.logger.warning(f"Permission denied: {path}")
            print(f"{Fore.YELLOW}Permission denied: {path}{Fore.RESET}")

    def _select_items(self, items: List[Path], parent_path: Path) -> List[Path]:
        """
        Prompt the user to select items from a list.

        Args:
            items (List[Path]): List of items to select from.
            parent_path (Path): Parent path of the items.

        Returns:
            List[Path]: List of selected items.
        """
        for i, item in enumerate(items, 1):
            print(f"{i}. ── {item.name}{'/' if item.is_dir() else ''}")

        print("-------------------")
        choice = input("Add: (A)ll or comma-separated numbers: ").strip().lower()

        if choice == 'a':
            self.logger.info(f"All items selected in {parent_path}")
            return items
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected = [items[i] for i in indices if 0 <= i < len(items)]
                self.logger.info(f"Selected items in {parent_path}: {', '.join(str(item) for item in selected)}")
                return selected
            except ValueError:
                self.logger.warning("Invalid input. Please try again.")
                print(f"{Fore.YELLOW}Invalid input. Please try again.{Fore.RESET}")
                return self._select_items(items, parent_path)
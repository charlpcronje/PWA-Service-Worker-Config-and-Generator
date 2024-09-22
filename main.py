# main.py

import argparse
import logging
from typing import NoReturn
from colorama import init, Fore

from config_manager import ConfigManager
from file_analyzer import FileAnalyzer
from service_worker_generator import ServiceWorkerGenerator
from utils import setup_logging

class ServiceWorkerApp:
    """
    Main application class for generating service worker configuration and script.

    Attributes:
        logger (logging.Logger): Logger for the application.
        config_manager (ConfigManager): Manages configuration loading and generation.
        file_analyzer (FileAnalyzer): Analyzes file structure.
        sw_generator (ServiceWorkerGenerator): Generates service worker script.
    """

    def __init__(self):
        """Initialize the ServiceWorkerApp."""
        self.logger = setup_logging()
        self.config_manager = ConfigManager(self.logger)
        self.file_analyzer = FileAnalyzer(self.logger)
        self.sw_generator = ServiceWorkerGenerator(self.logger)

    def run(self, args: argparse.Namespace) -> NoReturn:
        """
        Run the application.

        Args:
            args (argparse.Namespace): Command-line arguments.

        Returns:
            NoReturn: This method doesn't return.
        """
        try:
            if args.config:
                config = self.config_manager.load_config(args.config)
            else:
                config = self.config_manager.generate_config(args.root_path)

            analyzed_files = self.file_analyzer.analyze(config)
            sw_code = self.sw_generator.generate(analyzed_files)

            with open('service-worker.js', 'w') as f:
                f.write(sw_code)

            self.logger.info(f"{Fore.GREEN}Service worker generated: service-worker.js{Fore.RESET}")
            print(f"{Fore.GREEN}Service worker generated: service-worker.js{Fore.RESET}")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            print(f"{Fore.RED}An error occurred. Check the log file for details.{Fore.RESET}")
            raise

def main():
    """Entry point of the application."""
    init(autoreset=True)  # Initialize colorama

    parser = argparse.ArgumentParser(description="Generate service worker configuration and script")
    parser.add_argument("--config", help="Path to existing JSON config file")
    parser.add_argument("--root_path", help="Root path of the web application")
    args = parser.parse_args()

    if not args.config and not args.root_path:
        parser.error("Either --config or --root_path must be provided")

    app = ServiceWorkerApp()
    app.run(args)

if __name__ == "__main__":
    main()
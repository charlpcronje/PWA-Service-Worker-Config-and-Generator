# service_worker_generator.py

from typing import List
import logging
from colorama import Fore

class ServiceWorkerGenerator:
    """
    Class for generating the service worker script based on the configuration.

    Attributes:
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize the ServiceWorkerGenerator.

        Args:
            logger (logging.Logger): Logger instance.
        """
        self.logger = logger

    def generate(self, files_to_cache: List[str]) -> str:
        """
        Generate the service worker script.

        Args:
            files_to_cache (List[str]): List of files to be cached by the service worker.

        Returns:
            str: The generated service worker script.
        """
        cache_name = 'my-site-cache-v1'

        sw_code = f"""
        // Service Worker code
        const CACHE_NAME = '{cache_name}';
        const urlsToCache = {files_to_cache};

        self.addEventListener('install', (event) => {{
            event.waitUntil(
                caches.open(CACHE_NAME)
                    .then((cache) => cache.addAll(urlsToCache))
            );
        }});

        self.addEventListener('fetch', (event) => {{
            event.respondWith(
                caches.match(event.request)
                    .then((response) => {{
                        if (response) {{
                            return response;
                        }}
                        return fetch(event.request).then(
                            (response) => {{
                                if (!response || response.status !== 200 || response.type !== 'basic') {{
                                    return response;
                                }}
                                const responseToCache = response.clone();
                                caches.open(CACHE_NAME)
                                    .then((cache) => {{
                                        cache.put(event.request, responseToCache);
                                    }});
                                return response;
                            }}
                        );
                    }})
            );
        }});
        """

        self.logger.info("Service worker script generated")
        print(f"{Fore.GREEN}Service worker script generated{Fore.RESET}")
        return sw_code
import time

from prometheus_client import (
    REGISTRY,
    start_http_server,
)

from .collector import SkupperCollector
from .config import settings


def app():
    """Main entry point for the application script"""
    REGISTRY.register(
        SkupperCollector(
            service_controller=settings.service_controller,
            timeout=settings.service_controller_timeout,
        )
    )
    # TODO disable standard prometheus metrics
    start_http_server(port=settings.port)
    while True:
        time.sleep(5)


if __name__ == "__main__":
    app()

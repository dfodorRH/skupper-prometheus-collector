import logging
from collections.abc import (
    Callable,
    Generator,
    Mapping,
)
from typing import Any

import requests
from prometheus_client import Metric
from prometheus_client.core import (
    GaugeMetricFamily,
    InfoMetricFamily,
)

log = logging.getLogger(__name__)


def service_controller_stats(service_controller: str, timeout: int) -> dict[str, Any]:
    try:
        log.debug(f"Fetching data from service controller {service_controller}")
        response = requests.get(service_controller, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError("Unable to fetch data from service controller") from exc

    return response.json()


class SkupperCollector:
    def __init__(self, service_controller: str, timeout: int) -> None:
        self.service_controller = service_controller
        self.timeout = timeout

    def compile_metrics(
        self, stats: Mapping[str, list[Mapping[str, Any]]]
    ) -> Generator[Metric, None, None]:
        """Compute prometheus metrics based on service-controller stats."""
        log.debug("Compiling metrics")
        # site metrics
        skupper_spec = InfoMetricFamily(
            name="skupper_site_spec",
            documentation="Skupper version and site information",
            labels=["site_name", "namespace"],
        )
        skupper_outgoing_connections = GaugeMetricFamily(
            name="skupper_site_outgoing_connections",
            documentation="Number of outgoing site connections",
            labels=["site_name", "namespace"],
        )
        log.debug(f"Compiling site metrics for {len(stats['sites'])} sites")
        for site in stats["sites"]:
            skupper_spec.add_metric(
                [site["site_name"], site["namespace"]],
                {
                    "version": site["version"],
                    "site_id": site["site_id"],
                    "edge": "1" if site["edge"] else "0",
                    "gateway": "1" if site["gateway"] else "0",
                    "url": site["url"],
                },
            )
            skupper_outgoing_connections.add_metric(
                [site["site_name"], site["namespace"]], len(site["connected"])
            )

        log.debug("Compiling service metrics")
        # service metrics
        service_spec = InfoMetricFamily(
            name="skupper_service_spec", documentation="Service information"
        )
        for service in stats["services"]:
            service_spec.add_metric(
                [], {"address": service["address"], "protocol": service["protocol"]}
            )
        skupper_service_count = GaugeMetricFamily(
            name="skupper_service_count",
            documentation="Number of available skupper services",
            value=len(stats["services"]),
        )
        yield from [
            skupper_spec,
            skupper_outgoing_connections,
            service_spec,
            skupper_service_count,
        ]

    def collect(
        self,
        fetch_service_controller_stats_func: Callable[
            [str, int], Mapping[str, list[Mapping[str, Any]]]
        ] = service_controller_stats,
    ) -> Generator[Metric, None, None]:
        stats = fetch_service_controller_stats_func(
            self.service_controller, self.timeout
        )
        yield from self.compile_metrics(stats)

import json
from pathlib import Path

import httpretty as httpretty_module

from skupper_prometheus_collector import collector


def test_service_controller_stats(httpretty: httpretty_module) -> None:
    """Test service_controller_stats."""
    url = "http://service-controller:1234/foobar"

    httpretty.register_uri(
        httpretty.GET, url, body=json.dumps({"key": "value"}), content_type="text/json"
    )
    assert collector.service_controller_stats(url, 1) == {"key": "value"}


def test_skupper_collector_compile_metrics() -> None:
    """Test SkupperCollector.compile_metrics."""
    stats = json.loads((Path(__file__).parent / "fixtures/stats.json").read_text())
    skupper_collector = collector.SkupperCollector("http://service-controller:1234", 1)
    metrics = list(skupper_collector.compile_metrics(stats))
    assert len(metrics) == 4
    assert metrics[0].name == "skupper_site_spec"
    assert len(metrics[0].samples) == 2
    assert metrics[1].name == "skupper_site_outgoing_connections"
    assert len(metrics[1].samples) == 2
    assert metrics[2].name == "skupper_service_spec"
    assert len(metrics[2].samples) == 1
    assert metrics[3].name == "skupper_service_count"
    assert len(metrics[3].samples) == 1


def test_skupper_collector_collect() -> None:
    """Test SkupperCollector.collect."""

    def fake_request(url: str, timeout: int) -> dict:
        return {"key": "value"}

    skupper_collector = collector.SkupperCollector("http://service-controller:1234", 1)
    skupper_collector.compile_metrics = lambda _: []  # type: ignore
    assert (
        list(
            skupper_collector.collect(fetch_service_controller_stats_func=fake_request)
        )
        == []
    )

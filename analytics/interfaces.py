"""Analytics-specific interfaces and registries."""

from __future__ import annotations

from core.interfaces import MetricsCollector

METRICS_REGISTRY: dict[str, MetricsCollector] = {}


def register(name: str, collector: MetricsCollector) -> None:
    """Register a metrics collector implementation."""
    METRICS_REGISTRY[name] = collector


def get_collector(name: str) -> MetricsCollector | None:
    """Retrieve a collector by name."""
    return METRICS_REGISTRY.get(name)

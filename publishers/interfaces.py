"""Publisher-specific interfaces and registries."""

from __future__ import annotations

from core.interfaces import Publisher

PUBLISHER_REGISTRY: dict[str, Publisher] = {}


def register(name: str, publisher: Publisher) -> None:
    """Register a publisher implementation."""
    PUBLISHER_REGISTRY[name] = publisher


def get_publisher(name: str) -> Publisher | None:
    """Retrieve a publisher by name."""
    return PUBLISHER_REGISTRY.get(name)

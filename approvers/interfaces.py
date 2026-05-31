"""Approver-specific interfaces and registries."""

from __future__ import annotations

from core.interfaces import Approver

APPROVER_REGISTRY: dict[str, Approver] = {}


def register(name: str, approver: Approver) -> None:
    """Register an approver implementation."""
    APPROVER_REGISTRY[name] = approver


def get_approver(name: str) -> Approver | None:
    """Retrieve an approver by name."""
    return APPROVER_REGISTRY.get(name)

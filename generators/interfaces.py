"""Generator-specific interfaces and registries."""

from __future__ import annotations

from core.interfaces import ContentGenerator

# Registry populated at runtime by scanning generators/ directory.
# Example: {"carousel": CarouselGenerator(), "avatar_video": AvatarVideoGenerator()}
GENERATOR_REGISTRY: dict[str, ContentGenerator] = {}


def register(name: str, generator: ContentGenerator) -> None:
    """Register a generator implementation."""
    GENERATOR_REGISTRY[name] = generator


def get_generator(name: str) -> ContentGenerator | None:
    """Retrieve a generator by name."""
    return GENERATOR_REGISTRY.get(name)

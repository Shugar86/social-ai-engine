"""Core interfaces for Social AI Engine.

All modules implement these contracts. Do not change without discussion.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class PostStatus(str, Enum):
    """Lifecycle states of a post."""

    PENDING = "pending"                 # Generated, not yet queued
    WAITING_APPROVAL = "waiting_approval"  # In queue, waiting for human
    APPROVED = "approved"               # Ready to publish
    REJECTED = "rejected"               # Discarded
    PUBLISHING = "publishing"           # In progress
    PUBLISHED = "published"             # Live
    FAILED = "failed"                   # Publish error, needs retry
    SCHEDULED = "scheduled"             # Approved but waiting for time


class MediaType(str, Enum):
    """Types of media assets."""

    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    REEL = "reel"
    STORY = "story"


@dataclass
class MediaAsset:
    """A single media file (image or video)."""

    type: MediaType
    local_path: str | None = None       # Path on disk
    url: str | None = None              # Public URL after upload
    mime_type: str = "image/jpeg"
    alt_text: str = ""


@dataclass
class Analytics:
    """Post performance metrics."""

    impressions: int = 0
    reach: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    engagement_rate: float = 0.0
    collected_at: datetime | None = None


@dataclass
class Post:
    """The central entity: a piece of content ready for publishing."""

    id: str
    project: str                        # e.g. "doctor_yulia"
    content_type: str                   # e.g. "myth_bust", "tip_of_day"
    format: str                         # e.g. "carousel", "avatar_video"
    status: PostStatus = PostStatus.PENDING

    text: str = ""                      # Full text / article version
    caption: str = ""                   # Instagram caption (with hashtags)
    media: list[MediaAsset] = field(default_factory=list)

    scheduled_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    approved_at: datetime | None = None
    published_at: datetime | None = None
    published_url: str | None = None
    published_id: str | None = None     # Platform-specific post ID

    analytics: Analytics | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    rejection_reason: str | None = None


# ---------------------------------------------------------------------------
# Component interfaces
# ---------------------------------------------------------------------------

class ContentGenerator(ABC):
    """Generates content (text, images, video) for a given topic."""

    @abstractmethod
    async def generate(
        self,
        topic: str,
        content_type: str,
        project_config: dict[str, Any],
    ) -> Post:
        """Generate a Post from a topic and project configuration.

        Args:
            topic: The subject matter for this post.
            content_type: Template key (e.g. "myth_bust").
            project_config: Loaded contents of the project's config.yaml.

        Returns:
            A Post with status PENDING.
        """
        ...


class Publisher(ABC):
    """Publishes a Post to a social platform."""

    @abstractmethod
    async def publish(self, post: Post, credentials: dict[str, Any]) -> str:
        """Publish the post and return a platform-specific post ID or URL.

        Args:
            post: The approved post to publish.
            credentials: Platform credentials (e.g. access_token, ig_user_id).

        Returns:
            Platform post ID or permalink.

        Raises:
            PublishError: If publication fails.
        """
        ...

    @abstractmethod
    async def health_check(self, credentials: dict[str, Any]) -> bool:
        """Verify credentials are valid."""
        ...


class Approver(ABC):
    """Handles human approval workflow."""

    @abstractmethod
    async def send_for_approval(self, post: Post) -> None:
        """Send post preview to the approver (e.g. Telegram bot)."""
        ...

    @abstractmethod
    async def get_decision(self, post_id: str) -> ApprovalDecision | None:
        """Poll or wait for a decision on the post.

        Returns None if no decision yet.
        """
        ...


@dataclass
class ApprovalDecision:
    """Result of human approval."""

    post_id: str
    decision: str                       # "approve" | "reject" | "edit"
    edited_caption: str | None = None   # New caption if decision == "edit"
    reason: str | None = None           # Optional rejection reason
    publish_now: bool = False           # Bypass scheduled_at


class Queue(ABC):
    """Persistent storage for posts awaiting approval or publishing."""

    @abstractmethod
    async def enqueue(self, post: Post) -> None:
        """Add a post to the queue."""
        ...

    @abstractmethod
    async def update(self, post: Post) -> None:
        """Update post status and fields."""
        ...

    @abstractmethod
    async def get(self, post_id: str) -> Post | None:
        """Fetch a post by ID."""
        ...

    @abstractmethod
    async def list_by_status(
        self,
        project: str | None = None,
        status: PostStatus | None = None,
        limit: int = 50,
    ) -> list[Post]:
        """List posts filtered by project and/or status."""
        ...


class Scheduler(ABC):
    """Decides WHEN to generate and publish content."""

    @abstractmethod
    async def next_topic(self, project: str) -> dict[str, Any] | None:
        """Return the next scheduled topic for a project, or None."""
        ...

    @abstractmethod
    async def is_publish_time(self, post: Post) -> bool:
        """Check if the post's scheduled_at has been reached."""
        ...


class MetricsCollector(ABC):
    """Fetches performance data from social platforms."""

    @abstractmethod
    async def collect(self, post: Post, credentials: dict[str, Any]) -> Analytics:
        """Fetch analytics for a published post."""
        ...

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import uuid

class ChannelType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    PUSH = "push"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    QUEUED = "queued"

@dataclass(frozen=True)
class NotificationRequest:
    """The input data required to trigger a notification."""
    user_id: str
    channel: ChannelType
    template_id: str
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1  # 0=Low, 1=Normal, 2=High

@dataclass
class NotificationLog:
    """Internal representation of a processed notification for auditing."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request: NotificationRequest = None
    status: NotificationStatus = NotificationStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    provider_response: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

from typing import Protocol, Dict, Any
from .entities import NotificationLog, ChannelType

class TemplateRenderer(Protocol):
    """Interface for a system that converts data into text/html."""
    def render(self, template_id: str, context: Dict[str, Any]) -> str:
        ...

class NotificationProvider(Protocol):
    """Interface for a 3rd party sender (SendGrid, Twilio, etc)."""
    async def send(self, destination: str, content: str) -> Dict[str, Any]:
        """
        Returns metadata from the provider (e.g., message_id)
        Raises DeliveryFailureError on failure.
        """
        ...

class UserProfileGateway(Protocol):
    """Interface to fetch user contact info (decoupled from the User Service)."""
    async def get_contact_info(self, user_id: str, channel: ChannelType) -> str:
        """Returns email address, phone number, or webhook URL."""
        ...

class NotificationRepository(Protocol):
    """Interface for persisting notification logs."""
    async def save(self, notification: NotificationLog) -> None:
        ...

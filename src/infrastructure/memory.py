from typing import Dict, List
from src.core.interfaces import UserProfileGateway, NotificationRepository
from src.core.entities import ChannelType, NotificationLog
from src.core.exceptions import NotificationError

class InMemoryUserGateway(UserProfileGateway):
    def __init__(self):
        # Mock database of users
        self._users = {
            "user_123": {
                ChannelType.EMAIL: "alice@example.com",
                ChannelType.SMS: "+15550199"
            },
            "user_456": {
                ChannelType.EMAIL: "bob@example.com"
            }
        }

    async def get_contact_info(self, user_id: str, channel: ChannelType) -> str:
        user = self._users.get(user_id)
        if not user:
            raise NotificationError(f"User {user_id} not found")
        
        contact = user.get(channel)
        if not contact:
            raise NotificationError(f"User {user_id} has no contact info for {channel}")
        
        return contact

class InMemoryRepository(NotificationRepository):
    def __init__(self):
        self._storage: List[NotificationLog] = []

    async def save(self, notification: NotificationLog) -> None:
        self._storage.append(notification)
        # In a real app, this would be an INSERT statement
        print(f"[DB Persist] Saved log {notification.id} | Status: {notification.status}")

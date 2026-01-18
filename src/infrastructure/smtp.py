import logging
from email.message import EmailMessage
from typing import Dict, Any
import aiosmtplib

from src.core.interfaces import NotificationProvider
from src.core.exceptions import DeliveryFailureError

logger = logging.getLogger(__name__)

class SmtpEmailProvider(NotificationProvider):
    def __init__(self, hostname: str, port: int, use_tls: bool = False):
        self.hostname = hostname
        self.port = port
        self.use_tls = use_tls

    async def send(self, destination: str, content: str) -> Dict[str, Any]:
        message = EmailMessage()
        message["From"] = "noreply@nexus-notify.local"
        message["To"] = destination
        message["Subject"] = "Notification from Nexus"
        message.set_content(content, subtype="html")

        try:
            # Connect and send asynchronously
            async with aiosmtplib.SMTP(hostname=self.hostname, port=self.port, use_tls=self.use_tls) as smtp:
                response = await smtp.send_message(message)
                
            return {
                "provider": "smtp", 
                "host": self.hostname, 
                "response": str(response)
            }
            
        except Exception as e:
            # Wrap low-level network errors in our Domain Exception
            logger.error(f"SMTP Error: {e}")
            raise DeliveryFailureError(f"Failed to send email to {destination}") from e

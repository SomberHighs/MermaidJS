import logging
from typing import Dict
from .entities import NotificationRequest, NotificationLog, NotificationStatus, ChannelType
from .interfaces import (
    NotificationProvider, 
    TemplateRenderer, 
    UserProfileGateway, 
    NotificationRepository
)
from .exceptions import ProviderNotFoundError, DeliveryFailureError

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(
        self,
        providers: Dict[ChannelType, NotificationProvider],
        renderer: TemplateRenderer,
        user_gateway: UserProfileGateway,
        repository: NotificationRepository
    ):
        self.providers = providers
        self.renderer = renderer
        self.user_gateway = user_gateway
        self.repository = repository

    async def send_notification(self, request: NotificationRequest) -> NotificationLog:
        """
        The main use case: Validates, Renders, Resolves User, and Sends.
        """
        # 1. Initialize Log
        log = NotificationLog(request=request)
        
        try:
            # 2. Resolve Provider for Channel
            provider = self.providers.get(request.channel)
            if not provider:
                raise ProviderNotFoundError(f"No provider for {request.channel}")

            # 3. Fetch User Contact Info (e.g., email address)
            destination = await self.user_gateway.get_contact_info(
                request.user_id, request.channel
            )

            # 4. Render Content
            content = self.renderer.render(request.template_id, request.context)

            # 5. Send (Async operation)
            provider_meta = await provider.send(destination, content)
            
            # 6. Update Success State
            log.status = NotificationStatus.SENT
            log.provider_response = provider_meta
            logger.info(f"Notification {log.id} sent to {request.user_id}")

        except Exception as e:
            # 7. Handle Failure Gracefully
            log.status = NotificationStatus.FAILED
            log.error_message = str(e)
            logger.error(f"Notification {log.id} failed: {e}")
            
            # Re-raise if you want the API to return 500, 
            # or swallow if you want to just log it.
            if isinstance(e, (ProviderNotFoundError, DeliveryFailureError)):
                raise e
            raise DeliveryFailureError(f"Unexpected error: {e}") from e

        finally:
            # 8. Persist Log (Audit Trail)
            await self.repository.save(log)
        
        return log

class NotificationError(Exception):
    """Base exception for all notification domain errors."""
    pass

class TemplateNotFoundError(NotificationError):
    """Raised when a requested template ID does not exist."""
    pass

class ProviderNotFoundError(NotificationError):
    """Raised when no provider is configured for the requested channel."""
    pass

class DeliveryFailureError(NotificationError):
    """Raised when the downstream provider fails to deliver."""
    pass

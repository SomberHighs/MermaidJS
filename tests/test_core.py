import pytest
from unittest.mock import MagicMock, AsyncMock
from src.core.services import NotificationService
from src.core.entities import NotificationRequest, ChannelType, NotificationStatus
from src.core.exceptions import ProviderNotFoundError

# Fixture: Sets up the Service with Mock dependencies before every test
@pytest.fixture
def mock_service():
    # 1. Mock the Provider
    mock_email = AsyncMock()
    mock_email.send.return_value = {"msg_id": "123"} # Simulate success

    providers = {ChannelType.EMAIL: mock_email}

    # 2. Mock the Renderer
    mock_renderer = MagicMock()
    mock_renderer.render.return_value = "<h1>Hello</h1>"

    # 3. Mock the User Gateway
    mock_gateway = AsyncMock()
    mock_gateway.get_contact_info.return_value = "test@example.com"

    # 4. Mock the Repository
    mock_repo = AsyncMock()

    service = NotificationService(providers, mock_renderer, mock_gateway, mock_repo)

    # Return the service AND the mocks so we can assert on them
    return service, mock_email, mock_repo

@pytest.mark.asyncio
async def test_successful_email_flow(mock_service):
    service, mock_email, mock_repo = mock_service

    req = NotificationRequest(
        user_id="user_123",
        channel=ChannelType.EMAIL,
        template_id="welcome.html"
    )

    # Act
    log = await service.send_notification(req)

    # Assert
    assert log.status == NotificationStatus.SENT
    mock_email.send.assert_called_once_with("test@example.com", "<h1>Hello</h1>")
    mock_repo.save.assert_called_once() # Verify audit log was saved

@pytest.mark.asyncio
async def test_fail_if_no_provider(mock_service):
    service, _, _ = mock_service

    # Request SMS, but our fixture only set up EMAIL
    req = NotificationRequest(
        user_id="user_123",
        channel=ChannelType.SMS, # <--- This will fail
        template_id="welcome.html"
    )

    # Act & Assert
    with pytest.raises(ProviderNotFoundError):
        await service.send_notification(req)

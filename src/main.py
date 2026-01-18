import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# Import Core Domain
from src.core.entities import NotificationRequest, ChannelType
from src.core.services import NotificationService
from src.core.exceptions import NotificationError

# Import Infrastructure Adapters
from src.infrastructure.smtp import SmtpEmailProvider
from src.infrastructure.templates import JinjaRenderer
from src.infrastructure.memory import InMemoryUserGateway, InMemoryRepository

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus")

# --- GLOBAL STATE (Simulated singleton for the app lifespan) ---
class AppState:
    service: NotificationService = None

state = AppState()

# --- LIFESPAN (Startup/Shutdown Logic) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Adapters
    # In a real app, config would come from Pydantic Settings/Env Vars
    email_provider = SmtpEmailProvider(hostname="localhost", port=1025) 
    
    # We map channels to specific providers
    providers = {
        ChannelType.EMAIL: email_provider,
        # ChannelType.SMS: TwilioProvider(...), # Future extension
    }
    
    renderer = JinjaRenderer(template_dir="templates")
    user_gateway = InMemoryUserGateway()
    repository = InMemoryRepository()

    # 2. Inject Dependencies into the Service
    state.service = NotificationService(
        providers=providers,
        renderer=renderer,
        user_gateway=user_gateway,
        repository=repository
    )
    
    logger.info("Nexus Notification Service Initialized")
    yield
    # Shutdown logic (close DB connections, etc) goes here
    logger.info("Shutting down...")

# --- API DEFINITION ---
app = FastAPI(title="Nexus-Notify", lifespan=lifespan)

# --- DTOs (Data Transfer Objects) for the API ---
class ApiRequest(BaseModel):
    user_id: str
    channel: ChannelType
    template_id: str
    context: dict

# --- DEPENDENCY INJECTION ---
async def get_service() -> NotificationService:
    if not state.service:
        raise RuntimeError("App not initialized")
    return state.service

# --- ROUTES ---
@app.post("/v1/notify", status_code=202)
async def send_notification(
    payload: ApiRequest, 
    service: NotificationService = Depends(get_service)
):
    try:
        # Convert Pydantic API Model -> Domain Entity
        # This keeps our Domain clean of FastAPI dependencies
        domain_request = NotificationRequest(
            user_id=payload.user_id,
            channel=payload.channel,
            template_id=payload.template_id,
            context=payload.context
        )

        log = await service.send_notification(domain_request)
        
        return {
            "status": "success", 
            "notification_id": log.id,
            "provider_response": log.provider_response
        }

    except NotificationError as e:
        # Map Domain Errors to HTTP Status Codes
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected system error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

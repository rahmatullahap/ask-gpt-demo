from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.schema.ask_schema import AskBody, AskResponse
from app.services.open_ai_service import OpenAiService

router = APIRouter(
    prefix="/ask",
    tags=["ask"],
)

@router.post("/", response_model=AskResponse)
@inject 
async def ask(ask_body: AskBody, service: OpenAiService = Depends(Provide[Container.open_ai_service])):
    return service.chat_completion(ask_body)

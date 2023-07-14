from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.schema.ask_schema import AskBody, AskResponse, DocBody, DocResponse
from app.services.open_ai_service import OpenAiService
from app.services.supabase_service import SupabaseService

router = APIRouter(
    prefix="/ask",
    tags=["ask"],
)

@router.post("/", response_model=AskResponse)
@inject
async def ask(ask_body: AskBody, service: OpenAiService = Depends(Provide[Container.open_ai_service])):
    return service.chat_completion(ask_body)

@router.post("/document", response_model=DocResponse)
@inject
async def document(body: DocBody, service: SupabaseService = Depends(Provide[Container.supabase_service])):
    return service.get_document(Container.supabase, body)

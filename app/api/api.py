from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.container import Container
from app.schema.api_schema import AskBody, AskResponse
from app.schema.auth_schema import UserContext
from app.services.open_ai_service import OpenAiService
from app.core.dependencies import get_context
from app.core.exceptions import AuthError

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

@router.get("/healthz")
@inject
async def healthz():
    return "OK"

@router.get("/ask")
@inject
async def ask(
    ask_body: AskBody = Depends(),
    current_user: UserContext = Depends(get_context),
    service: OpenAiService = Depends(Provide[Container.open_ai_service])
):
    if current_user is None or current_user["email"] is None:
        return AuthError(detail="Invalid token or expired token.")

    question = {
        "question": ask_body.question,
        "lang": ask_body.lang,
    }
    res = await service.ask(question)
    return {
        "data": res
    }

@router.get("/ask-stream", response_model=AskResponse)
@inject
def ask_stream(
    ask_body: AskBody = Depends(),
    current_user: UserContext = Depends(get_context),
    service: OpenAiService = Depends(Provide[Container.open_ai_service])
):
    if current_user is None or current_user["email"] is None:
        return AuthError(detail="Invalid token or expired token.")

    question = {
        "question": ask_body.question,
        "lang": ask_body.lang,
    }
    return StreamingResponse(service.ask_stream(question), media_type='text/event-stream')

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.container import Container
from app.schema.api_schema import AskBody, AskResponse, DocBody, DocResponse
from app.services.open_ai_service import OpenAiService
from app.services.supabase_service import SupabaseService

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
    service: OpenAiService = Depends(Provide[Container.open_ai_service])
):
    question = {
        "question": ask_body.question,
        "lang": ask_body.lang,
    }
    res = await service.ask(question)
    return {
        "data": res
    }

# , response_model=AskResponse
@router.get("/ask-stream")
@inject
def ask_stream(
    ask_body: AskBody = Depends(),
    service: OpenAiService = Depends(Provide[Container.open_ai_service])
):
    # check user context
    # from auth bearer

    # TODO ask stream
    # count res time

    # return {
    #     "data": res
    # }

    question = {
        "question": ask_body.question,
        "lang": ask_body.lang,
    }
    return StreamingResponse(service.ask_stream(question), media_type='text/event-stream')


@router.post("/document", response_model=DocResponse)
@inject
async def document(body: DocBody, service: SupabaseService = Depends(Provide[Container.supabase_service])):
    return service.get_document(Container.supabase, body)

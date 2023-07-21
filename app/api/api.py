from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Response
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


@router.get("/cookie/set")
@inject
async def cookie_set(response: Response):
    response.set_cookie(key="LIA_SESSION_ID", value="true",
                        max_age=60, secure=True, samesite="None")
    return None


@router.get("/cookie/check")
@inject
async def cookie_check(request: Request):
    test_cookie = request.cookies.get("LIA_SESSION_ID")
    ok = False
    if test_cookie:
        ok = True
    return {
        "Ok": ok
    }


@router.post("/ask")
@inject
async def ask(
    ask_body: AskBody,
    ctx: UserContext = Depends(get_context),
    service: OpenAiService = Depends(Provide[Container.open_ai_service])
):
    with ctx["tracer"].start_as_current_span(name="service.ask") as span:
        ctx["span"] = span
        if ctx is None or ctx["email"] is None:
            raise AuthError(detail="Invalid token or expired token.")

        span.set_attribute("user.email", ctx["email"])

        question = {
            "question": ask_body.question,
            "lang": ask_body.lang,
        }
        span.set_attribute("question", ask_body.question)
        res = await service.ask(ctx, question)
        return {
            "data": res
        }


@router.get("/ask", response_model=AskResponse)
@inject
def ask_stream(
    ask_body: AskBody = Depends(),
    ctx: UserContext = Depends(get_context),
    service: OpenAiService = Depends(Provide[Container.open_ai_service])
):
    with ctx["tracer"].start_as_current_span(name="service.ask_stream") as span:
        ctx["span"] = span
        if ctx is None or ctx["email"] is None:
            raise AuthError(detail="Invalid token or expired token.")

        span.set_attribute("user.email", ctx["email"])

        question = {
            "question": ask_body.question,
            "lang": ask_body.lang,
        }
        span.set_attribute("question", ask_body.question)
        return StreamingResponse(service.ask_stream(ctx, question), media_type='text/event-stream')

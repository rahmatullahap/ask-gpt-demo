import json
import pytest
from opentelemetry import trace

from app.services import *
from app.repository import *
from app.schema.api_schema import AskBody
from app.schema.auth_schema import UserContext

@pytest.mark.asyncio
async def test_ask():
    question: AskBody = {
        "question": "apa saja yang diatur uu cipta kerja?",
        "lang": "id",
    }
    ctx: UserContext = {
        "email": "tes@myemail.com",
        "span": None,
        "tracer": trace.get_tracer("test")
    }
    supabase_repository = SupabaseRepository()
    service = OpenAiService(supabase_repository=supabase_repository)
    res = await service.ask(ctx, question)
    assert res["answer"] is not None

@pytest.mark.asyncio
async def test_ask_eng():
    question: AskBody = {
        "question": "apa saja yang diatur uu cipta kerja?",
        "lang": "eng",
    }
    ctx: UserContext = {
        "email": "tes@myemail.com",
        "span": None,
        "tracer": trace.get_tracer("test")
    }
    supabase_repository = SupabaseRepository()
    service = OpenAiService(supabase_repository=supabase_repository)
    res = await service.ask(ctx, question)
    assert res["answer"] is not None

@pytest.mark.asyncio
async def test_ask_stream():
    question: AskBody = {
        "question": "apa saja yang diatur uu cipta kerja?",
        "lang": "id",
    }
    ctx: UserContext = {
        "email": "tes@myemail.com",
        "span": None,
        "tracer": trace.get_tracer("test")
    }
    supabase_repository = SupabaseRepository()
    service = OpenAiService(supabase_repository=supabase_repository)
    result = ""
    async for chunk in service.ask_stream(ctx, question):
        result += str(chunk)
    assert result is not None

@pytest.mark.asyncio
async def test_ask_stream_no_answer():
    question: AskBody = {
        "question": "test?",
        "lang": "en",
    }
    ctx: UserContext = {
        "email": "tes@myemail.com",
        "span": None,
        "tracer": trace.get_tracer("test")
    }
    supabase_repository = SupabaseRepository()
    service = OpenAiService(supabase_repository=supabase_repository)
    result = ""
    async for chunk in service.ask_stream(ctx, question):
        res = json.loads(chunk)
        result += res["data"]["answer"]
    assert "sorry" in result

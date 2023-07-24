import json
import pytest
from opentelemetry import trace

from app.services import *
from app.repository import *

@pytest.mark.asyncio
async def test_ask():
    question = {
        "question": "apa saja yang diatur uu cipta kerja?",
        "lang": "id",
    }
    ctx = {
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
    question = {
        "question": "apa saja yang diatur uu cipta kerja?",
        "lang": "eng",
    }
    ctx = {
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
    question = {
        "question": "apa saja yang diatur uu cipta kerja?",
        "lang": "id",
    }
    ctx = {
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
    question = {
        "question": "test?",
        "lang": "en",
    }
    ctx = {
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
    assert "I'm sorry, but I cannot answer the question based on the given context" in result

import os
from typing import List
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Configs(BaseSettings):
    """Config"""
    # base
    PROJECT_NAME: str = "ask-gpt-demo"
    API: str = "/api"
    OPEN_API_KEY: str = os.environ['OPENAI_API_KEY']

    # supabase
    SUPABASE_URL: str = os.environ['SUPABASE_URL']
    SUPABASE_KEY: str = os.environ['SUPABASE_KEY']
    SUPABASE_DB: str = os.environ['SUPABASE_DB']

    # opentelemetry
    OTEL_SERVICE_NAME: str = os.environ['OTEL_SERVICE_NAME']
    OTEL_HONEYCOMB_API_KEY: str = os.environ['HONEYCOMB_API_KEY']
    OTEL_DEBUG: str = os.environ['OTEL_DEBUG']

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

configs = Configs()

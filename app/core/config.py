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
    OPEN_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')

    # supabase
    SUPABASE_URL: str = os.environ.get('SUPABASE_URL', '')
    SUPABASE_KEY: str = os.environ.get('SUPABASE_KEY', '')
    SUPABASE_DB: str = os.environ.get('SUPABASE_DB', '')

    # opentelemetry
    OTEL_SERVICE_NAME: str = os.environ.get('OTEL_SERVICE_NAME', '')
    OTEL_HONEYCOMB_API_KEY: str = os.environ.get('HONEYCOMB_API_KEY', '')
    OTEL_DEBUG: str = os.environ.get('OTEL_DEBUG', '')

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

configs = Configs()

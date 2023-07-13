import os
from typing import List
from pydantic import BaseSettings


class Configs(BaseSettings):
    """Config"""
    # base
    PROJECT_NAME: str = "ask-gpt-demo"
    API: str = "/api"
    OPEN_API_KEY: str = os.environ['OPENAI_API_KEY']

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

configs = Configs()

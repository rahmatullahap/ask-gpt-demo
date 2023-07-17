import openai
from dependency_injector import containers, providers
from supabase import create_client, Client

from app.core.config import configs
from app.services import *
from app.repository import *


class Container(containers.DeclarativeContainer):
    """Class container"""
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.api",
        ]
    )

    # open ai
    openai_key = configs.OPEN_API_KEY
    openai.api_key = openai_key

    # supabase
    url: str = configs.SUPABASE_URL
    key: str = configs.SUPABASE_KEY
    supabase: Client = create_client(url, key)

    supabase_repository = providers.Factory(SupabaseRepository)

    open_ai_service = providers.Factory(OpenAiService, supabase_repository=supabase_repository)
    supabase_service = providers.Factory(SupabaseService, supabase_repository=supabase_repository)

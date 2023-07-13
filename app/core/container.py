import openai
from dependency_injector import containers, providers

from app.core.config import configs
from app.services import *


class Container(containers.DeclarativeContainer):
    """Class container"""
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.ask",
        ]
    )

    openai_key = configs.OPEN_API_KEY
    openai.api_key = openai_key

    open_ai_service = providers.Factory(OpenAiService)
    # TODO add repository

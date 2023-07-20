import openai
from dependency_injector import containers, providers
from opentelemetry import trace
from honeycomb.opentelemetry import configure_opentelemetry, HoneycombOptions

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

    # open telemetry
    configure_opentelemetry(
        HoneycombOptions(
            debug= True if configs.OTEL_DEBUG == "True" else False,
            apikey= configs.OTEL_HONEYCOMB_API_KEY,
            service_name= configs.OTEL_SERVICE_NAME,
        )
    )
    # tracing
    tracer = trace.get_tracer(configs.OTEL_SERVICE_NAME)

    # repositories
    supabase_repository = providers.Factory(SupabaseRepository)
    open_ai_service = providers.Factory(OpenAiService, supabase_repository=supabase_repository)

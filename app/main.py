from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from opentelemetry import trace
from honeycomb.opentelemetry import configure_opentelemetry, HoneycombOptions

from app.api.routes import routers
from app.core.config import configs
from app.core.container import Container
from app.core.otel import OpenTelemetryMiddleware
from app.util.class_object import singleton



@singleton
class AppCreator:
    """App creator init"""
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        # set container
        self.container = Container()

        # set cors
        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # open telemetry
        configure_opentelemetry(
            HoneycombOptions(
                debug= True if configs.OTEL_DEBUG == "True" else False,
                apikey= configs.OTEL_HONEYCOMB_API_KEY,
                service_name= configs.OTEL_SERVICE_NAME,
            )
        )
        tracer = trace.get_tracer(configs.OTEL_SERVICE_NAME)
        self.app.add_middleware(OpenTelemetryMiddleware, tracer=tracer)

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(routers, prefix='')


app_creator = AppCreator()
app = app_creator.app
container = app_creator.container

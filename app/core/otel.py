from fastapi import FastAPI
from opentelemetry.trace import Tracer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request


class OpenTelemetryMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, tracer: Tracer):
        super().__init__(app)
        self._tracer = tracer

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        span_name = str(request["path"])
        with self._tracer.start_as_current_span(span_name):
            return await call_next(request)

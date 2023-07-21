from dependency_injector.wiring import inject
from fastapi import Depends
from pydantic import ValidationError
from opentelemetry import trace

from app.schema.auth_schema import Payload, UserContext
from app.core.security import decode_jwt, JWTBearer
from app.core.exceptions import AuthError
from app.core.config import configs


@inject
def get_context(
    token: str = Depends(JWTBearer())
) -> UserContext:
    try:
        tracer = trace.get_tracer(configs.OTEL_SERVICE_NAME)
        with tracer.start_as_current_span("authorization") as span:
            payload = decode_jwt(token=token)
            token_data = Payload(**payload)
            user: UserContext = {
                "email": token_data.eml,
                "name": token_data.unm,
                "tracer": tracer
            }
            return user
    except (ValidationError):
        raise AuthError(detail="Could not validate credentials")

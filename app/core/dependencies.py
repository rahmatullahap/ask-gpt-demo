from dependency_injector.wiring import inject
from fastapi import Depends
import jwt
from pydantic import ValidationError

from app.schema.auth_schema import Payload, UserContext
from app.core.security import decode_jwt, JWTBearer
from app.core.exceptions import AuthError


@inject
def get_context(
    token: str = Depends(JWTBearer())
) -> UserContext:
    try:
        payload = decode_jwt(token=token)
        token_data = Payload(**payload)
        user: UserContext = {
            "email": token_data.eml,
            "name": token_data.unm
        }
        return user
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")

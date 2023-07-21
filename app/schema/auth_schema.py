from typing import Optional, Type
from pydantic import BaseModel

class Payload(BaseModel):
    exp: int
    eml: str
    unm: str

class UserContext(BaseModel):
    email: str
    name: str
    span: Optional[Type] = None
    tracer: Optional[Type] = None

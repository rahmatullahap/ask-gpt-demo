from pydantic import BaseModel

class AskBody(BaseModel):
    message: str

class AskResponse(BaseModel):
    message: str
    success: bool

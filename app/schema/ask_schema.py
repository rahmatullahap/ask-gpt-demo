from pydantic import BaseModel

class AskBody(BaseModel):
    """Class Ask Body"""
    message: str

class AskResponse(BaseModel):
    """Class Ask Response"""
    message: str
    success: bool

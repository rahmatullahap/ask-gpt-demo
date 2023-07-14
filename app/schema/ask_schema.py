from typing import List, Optional
from pydantic import BaseModel

class AskBody(BaseModel):
    """Class Ask Body"""
    message: str

class AskResponse(BaseModel):
    """Class Ask Response"""
    message: str
    success: bool

class DocBody(BaseModel):
    """Class Doc Body"""
    id: int

class Document(BaseModel):
    """Class Document"""
    id: Optional[str]
    content: Optional[str]
    url: Optional[str]
    embedding: Optional[str]

class DocResponse(BaseModel):
    """Class Doc Response"""
    data: Optional[List[Document]]
    count: Optional[int]

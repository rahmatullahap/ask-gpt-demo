from typing import List, Optional
from pydantic import BaseModel

class AskBody(BaseModel):
    """Class Ask Body"""
    question: str
    lang: str

class AnswerResponse(BaseModel):
    """Class Answer Response"""
    answer: str
    source: str

class AskResponse(BaseModel):
    """Class Ask Response"""
    data: AnswerResponse

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

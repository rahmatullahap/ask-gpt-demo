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

class TokenUsage:
    """Class Token Usage"""
    def __init__(self, prompt_tokens=0, completion_tokens=0):
        self._prompt_tokens = prompt_tokens
        self._completion_tokens = completion_tokens
        self._total_tokens = prompt_tokens + completion_tokens

    @property
    def prompt_tokens(self):
        return self._prompt_tokens

    @prompt_tokens.setter
    def prompt_tokens(self, value):
        self._prompt_tokens = value
        self._total_tokens = self._prompt_tokens + self._completion_tokens

    @property
    def completion_tokens(self):
        return self._completion_tokens

    @completion_tokens.setter
    def completion_tokens(self, value):
        self._completion_tokens = value
        self._total_tokens = self._prompt_tokens + self._completion_tokens

    @property
    def total_tokens(self):
        return self._total_tokens

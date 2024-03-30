from pydantic import BaseModel
from typing import List
from typing import Any

class QueryExecutionException(Exception):
    def __init__(self, message):
        self.message = message


class ConnectionNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class QueryNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class PaginatedReturn(BaseModel):
    video: List[Any]
    page: int
    per_page: int


class SearchReturn(BaseModel):
    video: List[Any]
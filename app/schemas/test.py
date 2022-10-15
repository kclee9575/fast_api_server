from pydantic import BaseModel
from typing import List, Optional
from app.utils.geometry import AbstractPosition


class TestRequest(BaseModel):
    test : str 

class TestResponse(BaseModel):
    test : str

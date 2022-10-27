from pydantic import BaseModel
from typing import List, Optional
from app.utils.geometry import AbstractPosition


class UserAuth(BaseModel):
    user_id: str
    password : str

class UserOut(BaseModel):
    auth : str

class UserResponse(BaseModel):
    user_id : str
    password : str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Union, Any

class AuthManager:
    def __init__(self):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 day
        self.ALGORITHM = "HS256"
        self.JWT_SECRET_KEY ="test_jwt_key_value"  # scret_key # os.environ['JWT_SECRET_KEY']
        self.JWT_REFRESH_SECRET_KEY = "test_jwt_refresh_key_value" # refresh sceret_key # os.environ['JWT_REFRESH_SECRET_KEY']
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def decode_jwt(self, token: str):
        return jwt.decode(
            token, self.JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM]
        )

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)
    
    def create_access_token(
        self, user: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = (
                datetime.utcnow()
                + timedelta(hours=9)
                + timedelta(minutes=expires_delta)
            )
        else:
            expires_delta = (
                datetime.utcnow()
                + timedelta(hours=9)
                + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            )

        to_encode = {"exp": expires_delta, "user": str(user)} 
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(
        self, user: Union[str, Any], expires_delta: int = None
    ) -> str:
        if expires_delta is not None:
            expires_delta = (
                datetime.utcnow()
                + timedelta(minutes=expires_delta)
            )
        else:
            expires_delta = (
                datetime.utcnow()
                + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            )

        to_encode = {"exp": expires_delta, "user": str(user)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt


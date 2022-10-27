from app.services import auth_handler
from app.services.auth_handler import AuthHandler
from app.common.logger import logger
from jose import jwt
from pydantic import ValidationError
#from app.schemas import TokenPayload, SystemUser
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import AuthManager

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

async def get_current_user(token: str = Depends(reuseable_oauth)):
    auth_manager = AuthManager()
    auth_handler = AuthHandler()
    try:
        payload = auth_manager.decode_jwt(token)
        token_data = payload.get('user')

    except(jwt.JWTError, ValidationError):
        return {}

    user_id = token_data.replace("'", "").split(" ")[0].split("=")[1] # user_id 잘라내는방법 변경해야함..
    user = await auth_handler.get_user_auth(user_id )
    if user is None:
        return {}

    return user


class BaseController:
    def __init__(self):
        self._auth_handler = AuthHandler()
        self._auth_manager = AuthManager()
        
        self._logger = logger

    @classmethod
    def response(self, response, message, code):
        return {"result": response, "message": message, "code": code}

    
    
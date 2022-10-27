from cmath import log

from . import BaseController
from fastapi_utils.cbv import cbv as class_based_view
from fastapi_utils.inferring_router import InferringRouter
from app.common.exception.db_exception import *
from app.services.auth_handler import AuthHandler
from app.schemas.auth import UserAuth, UserOut

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm


auth_router = InferringRouter()
@class_based_view(auth_router)
class AuthController(BaseController):
    def __init__(self):
        super().__init__()
        #self._auth_handler = AuthHandler()
        
        
    # User 생성 (test/test) 존재하는 사용자
    @auth_router.post("/signup")
    async def create_user(self, request: UserAuth):
        user = await self._auth_handler.get_user_auth(request.user_id)
        if user is not None:
            return self.response("exist user", "", 400)
        
        user = {
            'user_id' : request.user_id,
            'password' : self._auth_manager.get_hashed_password( request.password )
        }

        await self._auth_handler.insert_user(user)
        
        return self.response(user,"",200)

    @auth_router.post("/login")
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        print("come here??")
        user = await self._auth_handler.get_user_auth(form_data.username)
        if user is None:
            return self.response("Incorrect User_id or Password", "", 400)

        hashed_password = user.password
        if not self._auth_manager.verify_password(form_data.password, hashed_password):
            return self.response("Incorrect User_id or Password", "", 400)

        return self.response({
            "access_token" : self._auth_manager.create_access_token(user),
            "refresh_token" : self._auth_manager.create_refresh_token(user)
        }, "", 200)

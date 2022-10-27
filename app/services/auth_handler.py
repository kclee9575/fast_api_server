from . import BaseHandler
from app.schemas.auth import *
from app.database.database import transactional


class AuthHandler(BaseHandler):
    def __init__(self):
        super().__init__()

    async def get_user_auth(self, user_id):
        # db로 부터 user정보 가져옴
        res = await self._auth_repository.get_user_info(user_id)
        if not res:
            return None
        return UserResponse(user_id=res.user_id, password=res.password)
    
    async def insert_user(self, user):
        return await self._auth_repository.insert_user(user)

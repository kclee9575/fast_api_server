from sqlalchemy import select, insert, update, delete
from . import BaseRepository

from app.database.models.user import User
from pydantic import BaseModel



class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class AuthRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, session):
        super().__init__(session, User)

    

    async def get_user_info(self, user_id):
        # 임시값 반환
        user = None
        if user_id == "test":
            user = User()
            user.user_id = "test"
            user.password = "$2b$12$zHJadoWbmGtSRZ0fF0i7quB6Y2ys4Wot3wjwKah0/BBaKoqQVzJ2e"
        
        return user


    async def insert_user(self, user):
        # db에 user 정보 저장
        user_uuid = "temp_uuid"
        return user_uuid
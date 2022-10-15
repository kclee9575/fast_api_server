from sqlalchemy import select, insert, update, delete
from . import BaseRepository

from app.database.models.test import Test
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from app.utils.timestamp import timestamp


class TestBase(BaseModel):
    pass


class TestCreate(TestBase):
    pass


class TestUpdate(TestBase):
    pass


class TestRepository(BaseRepository[Test, TestCreate, TestUpdate]):
    def __init__(self, session):
        super().__init__(session, Test)

    async def test_logic(self):
        ## Database Data
        test = Test(test = "test_123123")
        return test
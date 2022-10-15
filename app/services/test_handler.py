from . import BaseHandler
from app.database.database import transactional
from app.schemas.test import *


class TestHandler(BaseHandler):
    def __init__(self):
        super().__init__()

    @transactional
    async def test_logic(self, request):
        # request 상황에 맞춰 사용

        res = await self._test_repository.test_logic(         

        )
        return TestResponse(
            test = res.test
        )
    
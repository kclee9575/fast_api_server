from cmath import log

from . import BaseController
from fastapi_utils.cbv import cbv as class_based_view
from fastapi_utils.inferring_router import InferringRouter
from app.common.exception.db_exception import *
from fastapi import Depends
from . import get_current_user

test_router = InferringRouter()



@class_based_view(test_router)
class TestController(BaseController):
    def __init__(self):
        super().__init__()        
    
    @test_router.get("/test")
    async def test(self, user = Depends(get_current_user)):
        print( user ) # password 제거/ 필요한 정보있는경우 token 생성시 추가
        return self.response("test", "", 200)
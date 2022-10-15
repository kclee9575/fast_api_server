from cmath import log

from . import BaseController
from fastapi_utils.cbv import cbv as class_based_view
from fastapi_utils.inferring_router import InferringRouter
from app.common.exception.db_exception import *
from app.services.test_handler import TestHandler
from app.schemas.test import TestRequest

test_router = InferringRouter()


@class_based_view(test_router)
class DispatchController(BaseController):
    def __init__(self):
        super().__init__()
        self._test_handler = TestHandler()
        


    @test_router.post("/test")
    async def test(self, request: TestRequest):
        #self._logger.info(f"test logger")
        try :
            res = await self._test_handler.test_logic(request)
        except BadRequestException as e:
            self.response("", f"bad request : {str(e)}", 400) 
        # ...
        except Exception as e:
            self.response("", f"error : call your master : {str(e)}", 503)
        return self.response(res,"",200)
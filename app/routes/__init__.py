from app.services.test_handler import TestHandler
from app.common.logger import logger


class BaseController:
    def __init__(self):
        self._test_handler = TestHandler()
        
        self._logger = logger

    @classmethod
    def response(self, response, message, code):
        return {"result": response, "message": message, "code": code}

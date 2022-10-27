from app.services.auth_handler import AuthHandler
from app.common.logger import logger


class BaseController:
    def __init__(self):
        self._test_handler = AuthHandler()
        
        self._logger = logger

    @classmethod
    def response(self, response, message, code):
        return {"result": response, "message": message, "code": code}

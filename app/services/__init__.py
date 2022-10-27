from http.client import BAD_REQUEST
from app.common.exception.db_exception import *

from app.database.database import database
from app.repository.db.auth_repository import AuthRepository
from uuid import uuid4
from app.common.logger import logger

from app.schemas import *


class BaseHandler:
    def __init__(self):
        self._auth_repository = AuthRepository(database.session)
        self._logger = logger

    def get_unique_id(self):
        return str(uuid4())
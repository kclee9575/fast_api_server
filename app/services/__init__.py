from http.client import BAD_REQUEST
from app.common.exception.db_exception import *

from app.database.database import database
from app.repository.db.test_repository import TestRepository
from uuid import uuid4
from app.common.logger import logger

from app.schemas import *


class BaseHandler:
    def __init__(self):
        self._test_repository = TestRepository(database.session)
        self._logger = logger

    def get_unique_id(self):
        return str(uuid4())
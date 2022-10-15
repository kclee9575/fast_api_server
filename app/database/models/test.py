from app.database.database import Base
from sqlalchemy import Column, String, DateTime, func, Boolean


class Test(Base):
    __tablename__ = "test"

    test = Column(String(255), primary_key=True, nullable=False)
    
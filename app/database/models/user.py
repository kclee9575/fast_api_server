from app.database.database import Base
from sqlalchemy import Column, String, DateTime, func, Boolean


class User(Base):
    __tablename__ = "auth"

    user_id = Column(String(255), primary_key=True, nullable=False)
    password = Column(String(255), nullable=False)
    # 기타 등등
    
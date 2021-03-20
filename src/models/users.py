from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(Text)
    email = Column(String(30), unique=True)
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.username})>"

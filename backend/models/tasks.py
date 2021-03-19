from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from config.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, index=True)
    description = Column(Text)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.name})>"

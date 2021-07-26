from sqlalchemy import Column, Integer, Text
from app.database import Base


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(Text)

    def __init__(self, message=None):
        self.message = message

    def __repr__(self):
        return f'{self.message}'

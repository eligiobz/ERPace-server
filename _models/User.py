from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class User(Base):
    """ User:: Holds basic user information """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120))
    password = Column(String(120))
    level = Column(Integer)

    def __init__(self, username, password, level):
        self.username = username
        self.password = password
        self.level = level

    def __repr__(self):
        return {'username': self.username, 'pass': self.password, 'level': self.level}

    def getUser(self):
        return {'username': self.username, 'pass': self.password, 'level': self.level}

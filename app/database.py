from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hashlib import sha256

Base  = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    __username = Column("username", String)
    __hashed_password = Column("hashed_password", String)

    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__hashed_password = self.__hashing_password(password)

    def set_username(self, username: str) -> None:
        self.__username = username

    def set_password(self, password: str) -> None:
        self.__hashed_password = self.__hashing_password(password)

    def get_username(self) -> str:
        return self.__username

    def __hashing_password(self, password: str) -> str:
        hashed_password = sha256(password.encode())
        return hashed_password.hexdigest()
    
    def password_check(self, password: str) -> bool:
        hashed_password = self.__hashing_password(password)
        if self.__hashed_password == hashed_password:
            return True
        else:
            return False
        
    def get_json_without_password(self):
        json = {"id":self.id, "username":self.__username}

        return json
        
class Message(Base):
    __tablename__ = "messages"

    id = Column("id", Integer, primary_key=True)
    __text = Column("text", String)
    __sender_id = Column("sender_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
    __recipient_id = Column("recipient_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __init__(self, text: str, sender_id: int, recipient_id: int) -> None:
        self.__text = text
        self.__sender_id = sender_id
        self.__recipient_id = recipient_id
    
    def get_text(self) -> str:
        return self.__text
    
    def set_text(self, text: str) -> None:
        self.__text = text

    def get_sender_id(self) -> int:
        return self.__sender_id
    
    def set_sender_id(self, sender_id: int) -> None:
        self.__sender_id = sender_id

    def get_recipient_id(self) -> int:
        return self.__recipient_id
    
    def set_recipient_id(self, recipient_id: int) -> None:
        self.__recipient_id = recipient_id

    def get_json(self):
        json = {"text":self.__text, "sender_id": self.__sender_id, "recipient_id": self.__recipient_id}

        return json

engine = create_engine("sqlite:///db.sqlite3")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

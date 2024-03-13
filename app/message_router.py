from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import User
from repository import UserRepository, MessageRepository
from schemas import SMessage
from settings import JWTSetings
from typing import Annotated
import jwt

router = APIRouter(prefix="/api/v1/message", tags=["Messages"])
oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
user_repository = UserRepository()
message_repository = MessageRepository()
jwt_settings = JWTSetings()

def get_current_user(token: Annotated[str, Depends(oauth2_sheme)]):
    try:
        json_user = jwt.decode(token, jwt_settings.public_key, algorithms=[jwt_settings.algorithm])
        user = user_repository.search(json_user["username"], json_user["password"])
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("")
def send_a_message(current_user: Annotated[User, Depends(get_current_user)], message: SMessage):
    message_repository.add(message.text, current_user.id, message.recipient_id)

    return True

@router.get("/api/v1/message")
def get_message(current_user: Annotated[User, Depends(get_current_user)]):
    messages = message_repository.get_all()
    current_user_message = []
    for message in messages:
        if message.get_sender_id() == current_user.id or message.get_recipient_id() == current_user.id:
            current_user_message.append(message.get_json())

    return current_user_message

@router.delete("/api/v1/message")
def delete_message(current_user: Annotated[User, Depends(get_current_user)], id: int):
    message = message_repository.get(id)
    if message.get_sender_id() == current_user.id:
        message_repository.delete(id)
        return {"message": "The message has been deleted."}
    else:
        return {"message": "You cannot delete this message."}
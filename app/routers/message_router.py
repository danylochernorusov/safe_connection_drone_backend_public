from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from database import User
from repository import UserRepository, MessageRepository
from get_current_user import get_current_user
from schemas import SMessage, Response
from settings import JWTSettings
from typing import Annotated
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/api/v1/message", tags=["Messages"])
oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
user_repository = UserRepository()
message_repository = MessageRepository()
jwt_settings = JWTSettings()

@router.post("", status_code=status.HTTP_201_CREATED)
def send_a_message(current_user: Annotated[User, Depends(get_current_user)], message: SMessage) -> Response:
    recipient = user_repository.get(message.recipient_id)
    if recipient == None:
        return {"message": f"user with id - {message.recipient_id} does not exist."}
    message_repository.add(message.text, current_user.id, message.recipient_id)

    response = Response(response="the message has been sent")
    return response

@router.get("", status_code=status.HTTP_200_OK)
@cache(expire=60)
def get_messages(current_user: Annotated[User, Depends(get_current_user)], id_user: int | None = None) -> list:
    messages = message_repository.get_all()
    current_user_message = []
    for message in messages:
        if message.get_sender_id() == current_user.id or message.get_recipient_id() == current_user.id:
            if id_user != None:
                if message.get_sender_id() == id_user or message.get_recipient_id() == id_user:
                    current_user_message.append(message.get_json())
            else:
                current_user_message.append(message.get_json())

    return current_user_message

@router.delete("", status_code=status.HTTP_200_OK)
def delete_message(current_user: Annotated[User, Depends(get_current_user)], id: int) -> Response:
    message = message_repository.get(id)
    if message.get_sender_id() == current_user.id:
        message_repository.delete(id)
        response = Response(response="The message has been deleted.")
        return response
    else:
        response = Response(response="You cannot delete this message.")
        return response
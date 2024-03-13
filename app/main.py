from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import User
from repository import UserRepository, MessageRepository
from schemas import SUser, SMessage
from typing import Annotated
from settings import JWTSetings
import jwt

app = FastAPI()
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

@app.post("/api/v1/login/")
def login(from_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_repository.search(from_data.username, from_data.password)
        json_user = {"username": from_data.username, "password": from_data.password}
        token = jwt.encode(json_user, jwt_settings.private_key, jwt_settings.algorithm)
        return {"access_token": token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.post("/api/v1/registarion/")
def registarion(user: SUser):
    user_repository.add(user.username, user.password)

    return True

@app.get("/api/v1/users")
def get_users(current_user: Annotated[User, Depends(get_current_user)]):
    users = user_repository.get_all()
    list_users = []
    for user in users:
        list_users.append(user.get_json_without_password())

    return list_users

@app.post("/api/v1/message")
def send_a_message(current_user: Annotated[User, Depends(get_current_user)], message: SMessage):
    message_repository.add(message.text, current_user.id, message.recipient_id)

    return True

@app.get("/api/v1/message")
def get_message(current_user: Annotated[User, Depends(get_current_user)]):
    messages = message_repository.get_all()
    current_user_message = []
    for message in messages:
        if message.get_sender_id() == current_user.id or message.get_recipient_id() == current_user.id:
            current_user_message.append(message.get_json())

    return current_user_message

@app.delete("/api/v1/message")
def delete_message(current_user: Annotated[User, Depends(get_current_user)], id: int):
    message = message_repository.get(id)
    if message.get_sender_id() == current_user.id:
        message_repository.delete(id)
        return {"message": "The message has been deleted."}
    else:
        return {"message": "You cannot delete this message."}
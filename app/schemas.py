from pydantic import BaseModel

class SUser(BaseModel):
    username: str
    password: str

class SMessage(BaseModel):
    text: str
    recipient_id: int

class Response(BaseModel):
    response: str
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.repository import MessageRepository
import pytest

client = TestClient(app)
message_repository = MessageRepository()

jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QgdXNlciIsInBhc3N3b3JkIjoicGFzc3dvcmQifQ.IUx9KKZ1Qm_oSD4JtTgsO-Gp34R9biG4iaLeH6D6StZaakt8AkXSjrz5NKHh1Vvx6MzB4YL7L8mAEe2dsdA5PpxfQfp7Fs_yWDmbqlQk_v7xE5uyhIADOW3BktXDh2v-r_sV7JEiPsFqdrZyuKZlcXixb2p2wZUlURTaxrlsJtJ1nV5CLhFRdF6B5tw0iCGZ7hRF5E7yga_3PAk4WkIybZ-L5-einRAm5NBa21O2YluGHOi1VwXT2ZdVsv9d4hyz-ciijV1jf0Hstu1GRV5jk2NWCR00p6Z3axttnixWkG8EaDrKJm-JqJtTDRw9Z4A1bLxSDxi9cNwRL1Ny60tPI8kvxL4"

@pytest.fixture(scope="session", autouse=True)
def sutup_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    client.post("/api/v1/registarion/", json={"username": "test user", "password": "password"})
    client.post("/api/v1/registarion/", json={"username": "test user 2", "password": "password"})

    yield

    Base.metadata.drop_all(engine)

@pytest.fixture(scope="session", autouse=True)
def create_messages():
    message = {"text": "message", "recipient_id": 2}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt}"})

    message = {"text": "Hello!", "recipient_id": 2}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt}"})

def test_send_a_message():
    message = {"text": "message", "recipient_id": 2}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt}"})

    messages = message_repository.get_all()
    messages_json = [m.get_json() for m in messages]
    message["sender_id"] = 1
    message["id"] = messages[-1].id

    assert message in messages_json

def test_send_a_message_without_auth():
    message = {"text": "message", "recipient_id": 2}
    response = client.post("/api/v1/message", json=message)

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401

def test_get_message():
    response = client.get("/api/v1/message", headers={"Authorization": f"Bearer {jwt}"})

    messages = message_repository.get_all()
    messages_json = [message.get_json() for message in messages]

    assert response.json() == messages_json

def test_get_message():
    message = message_repository.get_all()[-1]

    client.delete("/api/v1/message", params={"id": message.id}, headers={"Authorization": f"Bearer {jwt}"})

    messages = message_repository.get_all()

    assert message not in messages

def test_delete_message_without_auth():
    response = client.delete("/api/v1/message")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.repository import MessageRepository, UserRepository
import pytest

client = TestClient(app)
message_repository = MessageRepository()
user_repository = UserRepository()
jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InBhc3N3b3JkIn0.pc8yd_sVdZn3gR2t4lt5ZrjM-qUQS656NP7VJmRjDrmfAk6ZnjbY-WwSNdughC0O5yutvBITJNdp5CcAdvvF3e78MhxER2aNG7mmh_piKVPqFSt9bW4KQrhIA-Qj-3UWe8x_RYC5ny1ooOZZwieB756qTBCMd0u27uNbCkktv4csSjNX6UahSPRXfIfPLSennmLhDl3prRb5KT7KH_sM1f2JZhFWPv_NDOX4BrQjf37rkoNMLFMKj9fvIED1DP3lUnNzm6bI7FhinWhJaHI9pey1AZOuEAb6ha8RJc9F2to7ZzJayVcfbP80KvaBnsVZ3CzBR_nI2UctQP2tnCFnXXtwHjM"

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    client.post("/api/v1/registarion/", json={"username": "test_user1", "password": "password"})
    client.post("/api/v1/registarion/", json={"username": "test_user2", "password": "password"})
    client.post("/api/v1/registarion/", json={"username": "test_user3", "password": "password"})

    yield

@pytest.fixture(scope="session", autouse=True)
def setup_caching():
    with TestClient(app) as c:
        print("caching is configured")

@pytest.fixture()
def create_message():
    message = {"text": "message", "recipient_id": 2}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt}"})

    message = {"text": "message", "recipient_id": 3}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt}"})

def test_send_a_message():
    message = {"text": "message", "recipient_id": 2}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt}"})

    messages = message_repository.get_all()
    message["id"] = messages[-1].id
    message["sender_id"] = messages[-1].get_sender_id()

    messages_json = [m.get_json() for m in messages]

    assert message in messages_json

def test_send_a_message_without_authorization():
    message = {"text": "message", "recipient_id": 2}
    response = client.post("/api/v1/message", json=message)

    assert response.json() == {"detail": "Not authenticated"}

def test_get_messages_from_specific_correspondence(create_message):
    response = client.get("/api/v1/message?id_user=2", headers={"Authorization": f"Bearer {jwt}"})

    messages = message_repository.get_all()
    all_messages_json = [message.get_json() for message in messages if message.get_sender_id() == 1 or message.get_recipient_id() == 1]
    messages_from_specific_correspondence_json = [message for message in all_messages_json if message["sender_id"] == 2 or message["recipient_id"] == 2]

    assert response.json() == messages_from_specific_correspondence_json

def test_delete_message(create_message):
    message = message_repository.get_all()[-1]

    client.delete("/api/v1/message", params={"id": message.id}, headers={"Authorization": f"Bearer {jwt}"})

    messages = message_repository.get_all()

    assert message not in messages

def test_delete_message_without_auth():
    response = client.delete("/api/v1/message")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401

def test_get_users():
    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {jwt}"})
    users = user_repository.get_all()
    users_json = [user.get_json_without_password() for user in users]

    assert response.json() == users_json

def test_get_users_without_auth():
    response = client.get("/api/v1/users")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401

def test_delete_users():
    client.delete("/api/v1/users?password=password", headers={"Authorization": f"Bearer {jwt}"})

    all_users = user_repository.get_all()
    all_users_json = [user.get_json_without_password() for user in all_users]

    deleted_user = {"id": 1, "username": "test_user1"}

    assert deleted_user not in all_users_json

def test_delete_users_without_auth():
    response = client.delete("/api/v1/users?password=password")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
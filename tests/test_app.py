from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.repository import MessageRepository, UserRepository
import pytest

client = TestClient(app)

message_repository = MessageRepository()
user_repository = UserRepository()

jwt_1 = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InBhc3N3b3JkIn0.pc8yd_sVdZn3gR2t4lt5ZrjM-qUQS656NP7VJmRjDrmfAk6ZnjbY-WwSNdughC0O5yutvBITJNdp5CcAdvvF3e78MhxER2aNG7mmh_piKVPqFSt9bW4KQrhIA-Qj-3UWe8x_RYC5ny1ooOZZwieB756qTBCMd0u27uNbCkktv4csSjNX6UahSPRXfIfPLSennmLhDl3prRb5KT7KH_sM1f2JZhFWPv_NDOX4BrQjf37rkoNMLFMKj9fvIED1DP3lUnNzm6bI7FhinWhJaHI9pey1AZOuEAb6ha8RJc9F2to7ZzJayVcfbP80KvaBnsVZ3CzBR_nI2UctQP2tnCFnXXtwHjM"
jwt_2 = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjIiLCJwYXNzd29yZCI6InBhc3N3b3JkIn0.aGrumNuiY2y21nnRpfhjwu_fxIpzrIhCgQ-iPYomgNQvzgnpCNcDCpJdKHdZMCufNyv7AAea5c4U7U_A0fRS1J-U8tDrrLeQIpqd2_NU7W4_wdVPffQ5yrcqH50KKMtZTYWa0YrU-3BT_urgrPoOWAjLMSYSDvbtAXfQJK1qYGiwxXoLWemFG1hIidh9FOuEz31aiaNqd86-Rvp0ihwGAUi5FfRc3kRzsgE61tCiiaydRlGP0S8CPudWJK7c4Aw81kf8yMBLLWKrZAbFrmSJiXi0pZvmd50HfswqrpI2MH1rLWanKue9zYAZAQPnxUEbnUlnzD0iHtztZdQf6PkXUyKyorM"
jwt_3 = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjMiLCJwYXNzd29yZCI6InBhc3N3b3JkIn0.GPfE-nixQygZ_rqEjhhGO33g6r7GEMkCYsbqb2pb1Z3R5dz0iwD6e8IeHNouSZzwWm6mvsFtA1-c1hD_TQxm5aEUbXWplyjxxqDDXyXJE2RwFuZCAJ0SB8U62j0WOej8I6OoQBvzyPYrK2p28n7xsrMca44WZTHCDB0VsNRCGhdTZrM9_rQnZXw53pjEAwcQT3YZF56FEqc7wPirjYvvjWlIM62KQmhDAuG5Er_VXVf0Tmytwqk0Yew_w4J706kgaZwidVaRavABwoGmaCFhzQCKmIUDxIt-eeny-pHzTCHzwGU7n55H-X45RkfkJLoTt3UpozUX0QD5stC3Q4sqJJH81yI"
jwt_list = [jwt_1, jwt_2, jwt_3]

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
    for i in range(1, 4):
        for j in range(1, 4):
            if j == i: continue

        message = {"text": "message", "recipient_id": j}
        client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt_list[i-1]}"})    

def test_send_a_message():
    message = {"text": "message", "recipient_id": 2}
    client.post("/api/v1/message", json=message, headers={"Authorization": f"Bearer {jwt_1}"})

    messages = message_repository.get_all()
    message["id"] = messages[-1].id
    message["sender_id"] = messages[-1].get_sender_id()

    messages_json = [m.get_json() for m in messages]

    assert message in messages_json

def test_send_a_message_without_authorization():
    message = {"text": "message", "recipient_id": 2}
    response = client.post("/api/v1/message", json=message)

    assert response.json() == {"detail": "Not authenticated"}

def test_get_all_messages(create_message):
    response = client.get("/api/v1/message", headers={"Authorization": f"Bearer {jwt_1}"})

    messages = message_repository.get_all()
    all_messages_json = [message.get_json() for message in messages if message.get_sender_id() == 1 or message.get_recipient_id() == 1]

    assert response.json() == all_messages_json

def test_get_messages_from_specific_correspondence(create_message):
    response = client.get("/api/v1/message?id_user=2", headers={"Authorization": f"Bearer {jwt_1}"})

    messages = message_repository.get_all()
    all_messages_json = [message.get_json() for message in messages if message.get_sender_id() == 1 or message.get_recipient_id() == 1]
    messages_from_specific_correspondence_json = [message for message in all_messages_json if message["sender_id"] == 2 or message["recipient_id"] == 2]

    assert response.json() == messages_from_specific_correspondence_json

def test_delete_message(create_message):
    all_messages = message_repository.get_all()
    messages_user = [message for message in all_messages if message.get_sender_id() == 1]
    message = messages_user[-1]

    client.delete("/api/v1/message", params={"id": message.id}, headers={"Authorization": f"Bearer {jwt_1}"})

    all_messages = message_repository.get_all()

    assert message not in all_messages

def test_delete_message_without_auth():
    response = client.delete("/api/v1/message")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401

def test_get_users():
    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {jwt_1}"})
    users = user_repository.get_all()
    users_json = [user.get_json_without_password() for user in users]

    assert response.json() == users_json

def test_get_users_without_auth():
    response = client.get("/api/v1/users")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401

def test_delete_users():
    client.delete("/api/v1/users?password=password", headers={"Authorization": f"Bearer {jwt_1}"})

    all_users = user_repository.get_all()
    all_users_json = [user.get_json_without_password() for user in all_users]

    deleted_user = {"id": 1, "username": "test_user1"}

    assert deleted_user not in all_users_json

def test_delete_users_without_auth():
    response = client.delete("/api/v1/users?password=password")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
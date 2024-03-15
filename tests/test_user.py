from fastapi.testclient import TestClient
from app.main import app
from app.repository import UserRepository

client = TestClient(app)
user_repository = UserRepository()

jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QgdXNlciIsInBhc3N3b3JkIjoicGFzc3dvcmQifQ.IUx9KKZ1Qm_oSD4JtTgsO-Gp34R9biG4iaLeH6D6StZaakt8AkXSjrz5NKHh1Vvx6MzB4YL7L8mAEe2dsdA5PpxfQfp7Fs_yWDmbqlQk_v7xE5uyhIADOW3BktXDh2v-r_sV7JEiPsFqdrZyuKZlcXixb2p2wZUlURTaxrlsJtJ1nV5CLhFRdF6B5tw0iCGZ7hRF5E7yga_3PAk4WkIybZ-L5-einRAm5NBa21O2YluGHOi1VwXT2ZdVsv9d4hyz-ciijV1jf0Hstu1GRV5jk2NWCR00p6Z3axttnixWkG8EaDrKJm-JqJtTDRw9Z4A1bLxSDxi9cNwRL1Ny60tPI8kvxL4"

def test_get_users():
    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {jwt}"})
    users = user_repository.get_all()
    users_json = [user.get_json_without_password() for user in users]

    assert response.json() == users_json

def test_get_users_without_auth():
    response = client.get("/api/v1/users")

    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
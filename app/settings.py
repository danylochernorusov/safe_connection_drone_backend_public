from pydantic import BaseModel
import os

class JWTSettings(BaseModel):
    private_key: str = f"-----BEGIN PRIVATE KEY-----\n{os.getenv("JWT_PRIVATE_KEY")}\n-----END PRIVATE KEY-----"
    public_key: str = f"-----BEGIN PUBLIC KEY-----\n{os.getenv("JWT_PUBLIC_KEY")}\n-----END PUBLIC KEY-----"
    algorithm: str = "RS256"

class DataBaseSettings(BaseModel):
    username: str = os.getenv("DB_USERNAME")
    password: str = os.getenv("DB_PASSWORD")
    host: str | int = os.getenv("DB_HOST")
    port: int = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
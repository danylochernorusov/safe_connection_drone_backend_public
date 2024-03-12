from pydantic import BaseModel
import os

class JWTSetings(BaseModel):
    private_key: str = f"-----BEGIN PRIVATE KEY-----\n{os.getenv("JWT_PRIVATE_KEY")}\n-----END PRIVATE KEY-----"
    public_key: str = f"-----BEGIN PUBLIC KEY-----\n{os.getenv("JWT_PUBLIC_KEY")}\n-----END PUBLIC KEY-----"
    algorithm: str = "RS256"
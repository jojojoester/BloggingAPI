from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from models import TokenData

# SECRET_KEY = os.getenv("secret_key")
SECRET_KEY = ("bd327066056b0334b59c80f52ca26443a7a3e2e486bf21c27105e4ff7ff6934f")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

async def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(api_key_header)):
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header. Must start with 'Bearer '",
        )
    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get("phone_number")
        if phone_number is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return TokenData(phone_number=phone_number)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

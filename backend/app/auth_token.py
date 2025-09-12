from fastapi import FastAPI, HTTPException, status, Depends
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from models import TokenData

#Declaring three crucial things: secretkety, algorithm and token expire minutes.
SECRET_KEY = os.getenv("secret_key")
ACCESS_TOKEN_EXPIRE_MINUTES = 10
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes = "bcrypt", deprecated = "auto")

oauth2_scheme = APIKeyHeader(name = "Authorization")

async def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY ,algorithm = ALGORITHM)
    return encoded_jwt


async def  get_current_user(token: str = Depends(oauth2_scheme)):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code = 401, detail = "Invalid Authorization header.")
    token = token.split(" ")[1]

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        header = {"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        email : str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email = email)

    except JWTError:
        raise credentials_exception
    
    return token_data




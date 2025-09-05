from fastapi import FastAPI
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta

#Declaring three crucial things: secretkety, algorithm and token expire minutes.
SECRET_KEY = os.getenv("secret_key")
ACCESS_TOKEN_EXPIRE_MINUTES = 10
ALGORITHM = "HS256"

async def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY ,algorithm = ALGORITHM)
    return encoded_jwt

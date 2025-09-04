#importing necessary modules
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from datetime import datetime, timedelta
from app.models import Token, TokenData

app = FastAPI(
    title = "Blogging API",
    description = "Blogging API that let's users to register, login, add blog posts, edit blog posts, delete blog posts, comment on other's blog post."
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")
#For security, we need to always declare three things:
#a. Algorithm
#b. Secret Key
#c. Access token 
JWT_SECRET_KEY = os.getenv("secret_key")
ALGORITHM = "256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


async def create_token(data:dict):
    # makes the copy of original data so that you do not make the changes in the original dictionary.
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire})
    #here, the encoded jwt is made with the mixture of JWT_SECRET_KEY, to_encode and algorithm.
    encoded_jwt = jwt.encode(JWT_SECRET_KEY, to_encode, algorithm = ALGORITHM)
    #returning the final encoded_jwt token
    return encoded_jwt



# function to get current users
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # this checks if the header really starts with a Bearer or not and after the Bearer, there is a valid access token or not.
    # if not, it raises an exception saying invalid authorization header.
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = token.split(" ")[1]  # extract actual token
    # this is how it works. It splits the strings into the list of available sub strings. For eg:
    # ["Bearer gdldgmdkgdgflkgmdfkgldgkgdlg3rjfeo"] changes this to ["Bearer","ffidfjsifwefuweinfscje"]

    # This will be raised if the token is invalid.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Verifies the token signature and expiration using secret key and algorithm.
        # if it is invalid, it raises JWTError..
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    return token_data





# @app.get("/register-user/")
# async def register_user():

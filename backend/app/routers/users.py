from fastapi import FastAPI, status, HTTPException, APIRouter
from typing import Optional
from models import RegisterUser, UserInDB
from database import users_collection
# from main import app
from passlib.context import CryptContext
router = APIRouter(tags = ["Users"])

#Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Creating register_user endpoints
@router.post("/register-user/", response_model = UserInDB, tags = ["Users"])
async def register_user(register: RegisterUser):
    if await users_collection.find_one({"username": register.username}):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Username already registered. Please use another username.")
    if await users_collection.find_one({"phone_number": register.phone_number}):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Phone number already registered. Try logging in.")
    
    #pwd is a passlib context.
    hashed_password = pwd_context.hash(register.password)
    user_dict = register.dict()
    user_dict["password"] = hashed_password
    await users_collection.insert_one(user_dict)

    return UserInDB(
    first_name=user_dict["first_name"],
    last_name=user_dict["last_name"],
    username=user_dict["username"]
)


#Creating login_user endpoints
# @router.get("/login-users/",)
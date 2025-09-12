from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pymongo import ReturnDocument
from database import users_collection
from models import RegisterUser, UserOut, UserInDB, UserLogin, Token, TokenData
from auth_token import create_token, get_current_user, APIKeyHeader

router = APIRouter(tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register-user/", response_model=UserOut)
async def register_user(register: RegisterUser):
    if await users_collection.find_one({"username": register.username}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered. Please use another username."
        )
    if await users_collection.find_one({"phone_number": register.phone_number}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered. Try logging in."
        )

    # Hash both password and confirm_password
    hashed_password = pwd_context.hash(register.password)
    hashed_confirm_password = pwd_context.hash(register.confirm_password)

    user_dict = register.dict()
    user_dict["password"] = hashed_password
    user_dict["confirm_password"] = hashed_confirm_password

    await users_collection.insert_one(user_dict)

    return UserOut(
        first_name=user_dict["first_name"],
        last_name=user_dict["last_name"],
        username=user_dict["username"]
    )


# Login
@router.post("/login-users/", response_model=Token)
async def login_users(userlogin: UserLogin):
    user = await users_collection.find_one({"phone_number": userlogin.phone_number})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_password = user["password"]
    if db_password.startswith("$2b$"):
        valid_password = pwd_context.verify(userlogin.password, db_password)
    else:
        valid_password = userlogin.password == db_password
        if valid_password:
            # Upgrade legacy plain password to hashed
            new_hashed = pwd_context.hash(userlogin.password)
            await users_collection.update_one({"_id": user["_id"]}, {"$set": {"password": new_hashed}})

    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_token(data={"phone_number": user["phone_number"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/get-me/", response_model=UserOut)
async def protected_route(current_user: TokenData = Depends(get_current_user)):
    # Fetch user data from DB using phone_number
    user = await users_collection.find_one({"phone_number": current_user.phone_number})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Return only safe fields
    return UserOut(
        first_name=user["first_name"],
        last_name=user["last_name"],
        username=user["username"],
        phone_number=user["phone_number"]
    )

# #router to update the existing user
# @router.put("/update-user/{phone_number}", response_model = UserInDB, tags = ["Users"])
# async def update_user(phone_number: str, edituser: UserInDB):
#     if await users_collection.find_one({"phone_number": edituser.phone_number}):
#         raise HTTPException(
#             status_code = status.HTTP_409_CONFLICT,
#             detail = "Phone number not registered. Try using valid phone numbers."
#         )
#     updated_user = await users_collection.find_one_and_update{

#     }


#router to delete the existing user
@router.delete("/delete_user/{phone_number}", tags = ["Users"])
async def delete_user(phone_number : str):
    user = await users_collection.delete_one({"phone_number" : phone_number})
    if user.deleted_count == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )
    return{"message": f"User with {phone_number} phone number deleted. "}
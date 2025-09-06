from pydantic import BaseModel, validator, Field
from typing import Optional
from fastapi import HTTPException, status

# class Token(BaseModel):
#     access_token = str
#     token_token = str

class TokenData(BaseModel):
    email : str


class RegisterUser(BaseModel):
    first_name : str
    last_name : str
    username : str
    phone_number : str = Field(..., min_length = 10)
    password : str
    confirm_password : str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Aashish",
                "last_name": "Rokka",
                "username": "jojo",
                "phone_number": "9849502928",
                "password": "jojo123",
                "confirm_password": "jojo123"
            }
        }

    @validator("confirm_password")
    def validate_password(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v



class UserInDB(BaseModel):
    first_name : str
    last_name : str
    username : str
    
    class Config:
        scheme_extra = {
            "examples": {
                "first_name": "Aashish",
                "last_name": "Rokka",
                "username": "jojo"
            }
        }


class UserLogin(BaseModel):
    phone_number : str
    password : str

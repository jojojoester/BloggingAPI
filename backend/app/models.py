from pydantic import BaseModel, Field
from typing import Optional

# This model represents the structure of a successful response when the user logs in.
class Token(BaseModel):
    # Corrected the syntax here to use a type annotation instead of an assignment.
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "examples": {
                "access_token": "fefjeurjf23rj239rifojmfovnd",
                "token_type": "bearer"
            }
        }

# This model represents the expected structure of the data contained within the JWT payload.
class TokenData(BaseModel):
    # Corrected the syntax for the Field, removing the extra colon.
    email: Optional[str] = Field(None, example="jojo@gmail.com")


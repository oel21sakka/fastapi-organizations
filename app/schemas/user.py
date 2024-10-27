from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str

    class Config:
        populate_by_name = True
        json_encoders = {str: str}

class User(UserBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {str: str}

class Token(BaseModel):
    access_token: str
    refresh_token: str

class RefreshToken(BaseModel):
    refresh_token: str

class TokenBlacklistRequest(BaseModel):
    refresh_token: str

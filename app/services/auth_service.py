from passlib.context import CryptContext
from app.schemas.user import UserCreate, UserInDB
from app.database.mongodb import users_collection
from app.core.token import create_access_token, create_refresh_token, verify_token
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(user: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    user_data = user.dict(exclude={"password"})
    user_data["hashed_password"] = hashed_password

    try:
        result = await users_collection.insert_one(user_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    
    created_user["_id"] = str(created_user["_id"])
    
    return UserInDB(**created_user)

async def get_user_by_email(email: str) -> UserInDB | None:
    user_dict = await users_collection.find_one({"email": email})
    if user_dict:
        user_dict["_id"] = str(user_dict["_id"])
        return UserInDB(**user_dict)
    return None

async def create_user_tokens(user: UserInDB):
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}

async def get_user_by_refresh_token(refresh_token: str):
    email = verify_token(refresh_token)
    if email:
        return await get_user_by_email(email)
    return None

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import TokenBlacklistRequest, UserCreate, User, Token, RefreshToken, UserSignIn
from app.services.auth_service import create_user, create_user_tokens, get_user_by_refresh_token
from app.core.security import authenticate_user, get_current_user
from app.core.token import verify_token, blacklist_token, is_token_blacklisted
from app.schemas.user import UserInDB

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    try:
        db_user = await create_user(user)
        return {'message': 'user created'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )

@router.post("/signin", response_model=Token)
async def signin(user: UserSignIn):
    user_db = await authenticate_user(user.email, user.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await create_user_tokens(user)

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: RefreshToken):
    if await is_token_blacklisted(refresh_token.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been blacklisted",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_refresh_token(refresh_token.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await create_user_tokens(user)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/token/blacklist", status_code=204)
async def blacklist_refresh_token(
    request: TokenBlacklistRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    subject = verify_token(request.refresh_token)
    if not subject:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    if subject != str(current_user.email):
        raise HTTPException(status_code=403, detail="Not authorized to blacklist this token")

    await blacklist_token(request.refresh_token)

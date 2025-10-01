from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.auth.model import User
from app.auth.schema import UserResponse, UserSignup, UserLogin, TokenResponse
from app.auth_util import get_current_user, get_token_from_header
from app.database import get_db
from app.global_constants import SuccessMessage, ErrorMessage
from app.jwt_utils import create_access_token, create_refresh_token, verify_token, blacklist_token
from app.security import verify_password, hash_password
from app.utils import get_response_schema

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer()

@router.post("/signup", response_model=UserResponse)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail=ErrorMessage.EMAIL_ALREADY_EXISTS.value)

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login
@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email,User.is_active == True).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_CREDENTIALS.value)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    user_response = UserResponse.model_validate(user)
    return_data={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_response
    }
    return get_response_schema(return_data, SuccessMessage.LOGIN_SUCCESS.value, status.HTTP_200_OK)



@router.post("/logout")
def logout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), token: str = Depends(get_token_from_header)):

    user_id = verify_token(token, db)
    if not user_id:
        raise HTTPException(status_code=401, detail=ErrorMessage.INVALID_TOKEN.value)
    if blacklist_token(token, db):
        return get_response_schema({}, SuccessMessage.LOGOUT_SUCCESS.value, status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=400, detail=ErrorMessage.LOGOUT_FAILED.value)



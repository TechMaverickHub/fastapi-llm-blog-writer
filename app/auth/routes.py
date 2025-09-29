from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app.auth.schema import UserResponse, UserSignup, UserLogin, TokenResponse
from app.global_constants import SuccessMessage
from app.jwt_utils import create_access_token, create_refresh_token
from app.security import verify_password, hash_password

from app.utils import get_response_schema

from app.auth.model import User
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

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
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    user_response = UserResponse.model_validate(user)
    return_data={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_response
    }
    return get_response_schema(return_data, SuccessMessage.LOGIN_SUCCESS.value, status.HTTP_200_OK)

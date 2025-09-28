from fastapi import FastAPI, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import engine, get_db
from app.exceptions import register_exception_handlers
from app.global_constants import SuccessMessage, ErrorMessage
from app.jwt_utils import create_access_token, create_refresh_token
from app.models import User
from app.schemas import UserSignup, TokenResponse, UserLogin, UserResponse
from app.security import hash_password, verify_password
from app.utils import get_response_schema

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    import traceback

    print("Error during table creation:")
    traceback.print_exc()

app = FastAPI(title="Blog API with Supabase", version="0.1.0", debug=True)

register_exception_handlers(app)

@app.post("/blog")
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return get_response_schema(new_blog, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)


@app.get("/blog-list", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    blog_list = db.query(models.Blog).order_by(models.Blog.updated_at.desc()).all()
    return get_response_schema(blog_list, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


@app.get("/blog/{id}")
def get_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Current user============")
    print(current_user.id)
    print(current_user.email)
    print(current_user.first_name)
    print(current_user.last_name)
    blog_record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_record:
        return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

    return get_response_schema(blog_record, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

@app.put("/blog/{id}")
def update_blog(id: int, blog: schemas.BlogUpdate, db: Session = Depends(get_db)):
    blog_record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.NOT_FOUND.value)

    blog_record.title = blog.title
    blog_record.content = blog.content
    db.add(blog_record)
    db.commit()
    db.refresh(blog_record)
    return get_response_schema(blog_record, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)


@app.delete("/blog/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog_record = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.NOT_FOUND.value)
    db.delete(blog_record)
    db.commit()
    return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)

@app.post("/signup", response_model=UserResponse)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    print("Existing user============")
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name
    )
    print("User============")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login
@app.post("/login", response_model=TokenResponse)
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

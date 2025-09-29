from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from app.auth.model import User
from app.auth_util import get_current_user
from app.blog.model import Blog
from app.blog.schema import BlogCreate, BlogResponse, BlogUpdate
from app.database import get_db
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.post("/blog")
def create_blog(blog: BlogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_blog = Blog(title=blog.title, content=blog.content, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return get_response_schema(new_blog, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)


@router.get("/blog-list", response_model=list[BlogResponse])
def get_blogs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog_list = db.query(Blog).filter(Blog.user_id == current_user.id).order_by(Blog.updated_at.desc()).all()
    return get_response_schema(blog_list, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


@router.get("/blog/{id}")
def get_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Current user============")
    print(current_user.id)
    print(current_user.email)
    print(current_user.first_name)
    print(current_user.last_name)
    blog_record = db.query(Blog).filter(Blog.id == id, Blog.user_id == current_user.id).first()
    if not blog_record:
        return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

    return get_response_schema(blog_record, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

@router.put("/blog/{id}")
def update_blog(id: int, blog: BlogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog_record = db.query(Blog).filter(Blog.id == id, Blog.user_id == current_user.id).first()
    if not blog_record:
        return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

    blog_record.title = blog.title
    blog_record.content = blog.content
    db.add(blog_record)
    db.commit()
    db.refresh(blog_record)
    return get_response_schema(blog_record, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)


@router.delete("/blog/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog_record = db.query(Blog).filter(Blog.id == id, Blog.user_id == current_user.id).first()
    if not blog_record:
        return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
    db.delete(blog_record)
    db.commit()
    return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)
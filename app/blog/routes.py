from fastapi import APIRouter, Depends, status, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.auth.model import User
from app.auth_util import get_current_user
from app.blog.model import Blog
from app.blog.schema import BlogCreate, BlogResponse, BlogUpdate, PaginatedResponse
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



@router.get("/blog-list-filter", response_model=PaginatedResponse[BlogResponse])
def get_blogs(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    sort_by: str = Query("updated_at", description="Field to sort by (e.g. created_at, updated_at, title)"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order: asc or desc"),
    search: str | None = Query(None, description="Search by blog title (case-insensitive)")
):
    """
    Retrieve a paginated, searchable, and sortable list of blogs.
    """

    # Base query
    query = db.query(Blog)

    # Optional search filter
    if search:
        query = query.filter(Blog.title.ilike(f"%{search}%"))

    # Sorting (safe dynamic field access)
    if hasattr(Blog, sort_by):
        sort_column = getattr(Blog, sort_by)
        query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))
    else:
        query = query.order_by(desc(Blog.updated_at))

    # Total count for pagination metadata
    total_blogs = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    blog_list = query.offset(offset).limit(limit).all()

    # Response with pagination metadata
    return get_response_schema(
        {
            "items": blog_list,
            "page": page,
            "limit": limit,
            "total": total_blogs,
            "pages": (total_blogs + limit - 1) // limit
        },
        SuccessMessage.RECORD_RETRIEVED.value,
        status.HTTP_200_OK
    )
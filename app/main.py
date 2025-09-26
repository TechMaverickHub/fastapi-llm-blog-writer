from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, SessionLocal
from app.exceptions import register_exception_handlers
from app.global_constants import SuccessMessage, ErrorMessage
from app.utils import get_response_schema

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    import traceback

    print("Error during table creation:")
    traceback.print_exc()

app = FastAPI(title="Blog API with Supabase", version="0.1.0", debug=True)

register_exception_handlers(app)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blogs")
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return get_response_schema(new_blog, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)


@app.get("/blogs-list", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return get_response_schema(blogs, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


@app.get("/blogs/{id}")
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessage.NOT_FOUND.value)

    return get_response_schema(blog, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

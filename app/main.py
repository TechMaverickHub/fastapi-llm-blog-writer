from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, SessionLocal
from app.global_constants import SuccessMessage
from app.utils import get_response_schema

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    import traceback
    print("Error during table creation:")
    traceback.print_exc()

app = FastAPI(title="Blog API with Supabase", version="0.1.0", debug=True)

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
    return get_response_schema(new_blog, SuccessMessage.RECORD_CREATED.value,  status.HTTP_201_CREATED)




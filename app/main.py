from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, SessionLocal

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


class Blog(BaseModel):
    title: str
    content: str


@app.post("/blogs")
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




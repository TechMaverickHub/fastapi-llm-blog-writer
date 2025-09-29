from fastapi import FastAPI

from app.auth import model as auth_models
from app.auth import routes as auth_routes
from app.blog import model as blog_models
from app.blog import routes as blog_routes
from app.llm import routes as llm_routes
from app.database import engine
from app.exceptions import register_exception_handlers

try:
    auth_models.Base.metadata.create_all(bind=engine)
    blog_models.Base.metadata.create_all(bind=engine)
except Exception as e:
    import traceback
    print("Error during table creation:")
    traceback.print_exc()

    print("Error during table creation:")
    traceback.print_exc()

app = FastAPI(title="Blog API with Supabase", version="0.1.0", debug=True)

register_exception_handlers(app)

# include routers
app.include_router(auth_routes.router)
app.include_router(blog_routes.router)
app.include_router(llm_routes.router)

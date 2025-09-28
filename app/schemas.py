from pydantic import BaseModel, EmailStr
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class BlogUpdate(BlogBase):
    pass


# Signup payload
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

# Login payload
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response payload after login (JWT + refresh token)
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Response payload for user details
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    model_config = {
        "from_attributes": True
    }

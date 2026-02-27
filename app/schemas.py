from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    # password: constr(min_length=8, max_length=72)  # enforce bcrypt limit

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:   # to tell pydantic model to work with sqlalchemy model 
        from_attributes = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----------------------------------------------------------------------
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# request body schema using inheritance
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# response body schema
class PostResponse(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:   # to tell pydantic model to work with sqlalchemy model 
        from_attributes = True 

class PostResponseWithVotes(BaseModel):
    post: PostResponse
    votes: int

    class Config:  
        from_attributes = True

# class PostResponseWrapper(BaseModel):
    # data: PostResponse #this will return resposne in {"data": {...}} format

# ---------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# ----------------------------------------------------------------------

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # type: ignore # direction of vote, 1 for upvote and 0 for downvote
    # Replaces conint(gt=0, le=100)
    # page: Annotated[int, Field(gt=0, le=1)] = 1

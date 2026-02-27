from fastapi import FastAPI, Response , status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# CURD operations using SQLAlchemy ORM   POST table
# Using SQLAlchemy ORM to retrieve all posts
@router.get("/",response_model= List[schemas.PostResponseWithVotes]) # response_model= schemas.PostResponse tries to shape it into one individual post, so to return list of posts we use List[]
# @router.get("/",response_model= List[schemas.PostResponse]) # response_model= schemas.PostResponse tries to shape it into one individual post, so to return list of posts we use List[]
def get_posts(db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit : int= 10,skip: int= 0,search: Optional[str]= ""):
    # posts= db.query(models.Post).all() # list of sqlalchemy objects posts by all users.
    # posts= db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #all  posts created by current user.
    
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #limit no. of posts
    # print(limit)
    posts= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)

    # return {"data": posts}  # returning list of dictionaries
    return [{"post": post, "votes": votes} for post, votes in posts]  # returning list of sqlalchemy objects directly

# Using SQLAlchemy ORM to create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 

    # new_post=models.Post(title= post.title, content = post.content, published= post.published) # this method is not suitable for large number of columns
    print(current_user.id) 
    print(current_user.email)
    print(post.dict()) # to convert pydantic model to dictionary
    new_post=models.Post(owner_id=current_user.id,**post.dict())# unpacking the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # new_post is a sqlalchemy object, so pydantic model can not read it directly because it expects a dictionary
    return new_post
    # return {"data": new_post} #if you want to wrap response into "data" then define a wrapper pydantic model in schemas.py

# retrieving a specific id using SQLAlchemy ORM with validation and its content with error handling
@router.get("/{id}",response_model= schemas.PostResponseWithVotes)
def get_post(id:int,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # post= db.query(models.Post).filter( models.Post.id == id).first()  #  to get the first match, if we do all() it will return data but will search entire database even if first match is found
    # print(post)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter( models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    post, votes = post
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action") # to check if the post belongs to the current user or not, if not then return 403 forbidden error
    return {"post": post, "votes": votes}

# to delete a specific id using SQLAlchemy ORM with validation and its content with error handling
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id== id)
    post= post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    # db.delete(post)
    post_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updating a specific id using SQLAlchemy ORM with validation and its content with error handling
@router.put("/{id}",response_model= schemas.PostResponse)
def update_post(id: int, post_data:schemas.PostCreate, db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()

    if post == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    # post_query.update({'title': 'updated title', 'content': 'updated content'},synchronize_session= False)
    post_query.update(post_data.dict(),synchronize_session= False)

    db.commit()
    return post

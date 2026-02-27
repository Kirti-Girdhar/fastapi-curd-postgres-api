# import time
# from typing import Optional, List
from fastapi import FastAPI, Depends #, Response , status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models #, schemas,utils
from .database import engine #,get_db ,SessionLocal
# from sqlalchemy.orm import Session
from .routers import post, user,auth, vote
from .config import settings

print(settings.database_username)

# connecting the models with database using sqlalchemy, it tells sqlalchemy to create the tables in the database if they do not exist already, using the models we have defined in models.py
# since we have alembic for database migrations, we can remove this line and use alembic to create tables in the database
# models.Base.metadata.create_all(bind = engine)

app= FastAPI()

origins=["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
                                             
@app.get("/")
def root():
    return {"message": "welcome to Fastapi !!"}

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# def get_db():
#     db= SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# database connection with psycopg2, 
# coppied in database.py so we can remove it from here
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='#Ki.rti2004',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection successfull")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("error: ", error)
#         time.sleep(3)

# # ---------------------------------------------------------------------

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title":"Favirote food", "content":"I love pizza", "id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id']== id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id']== id:
#             return i

# @app.get("/posts")
# def get_posts():
#     return {"data": my_posts} 

# Creating post using Body
# @app.post("/createposts")
# def create_Posts(payload: dict= Body(...)):
#     print(payload)
#     return{"message":"Post is created successfully"}  

# Creating post using Pydantic model
# @app.post("/posts")
# def create_Posts(new_post: Post):
#     print(new_post)
#     print(new_post.dict())
#     # print(new_post.rating)
#     return{"message":"new_post"}  

# storing the post in an array
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_Posts(post: Post):
#     post_dict = post.dict()
#     post_dict['id']= randrange(0,1000000)
#     my_posts.append(post_dict)
#     return{"data": post_dict}

# to retrieve a specific id
# @app.get("/posts/{id}")
# def get_post(id):
#     print(id)
#     return {"post_detail": f"Here is the post with id: {id}"}

# to retrieve a specific id with validation and its content
# @app.get("/posts/{id}")
# def get_post(id:int):
#     post=find_post(id)  # typecasting id to int from str
#     print(post)
#     return {"post_detail": post}

# to retrieve a specific id with validation and its content with error handling
# @app.get("/posts/{id}")
# def get_post(id:int, response: Response):
#     post=find_post(id)  # typecasting id to int from str
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")  # better way to handle exception
    
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id: {id} was not found"}  # another way to handle error 
#     print(post)
#     return {"post_detail": post}


# to delete a specific id with validation and its content with error handling
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     # find the index in the array that has required id
#     index= find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist") 
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# to update a specific id with validation and its content with error handling
# @app.put("/posts/{id}")
# def update_post(id:int, post: Post):
#     index= find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist") 
    
#     post_dict= post.dict()
#     post_dict['id']= id
#     my_posts[index]= post_dict
#     return {"message": f"post with id: {id} is updated"}

# --------------------------------------------------------------------

# Database connection with psycopg2 and CRUD operations : POST table
# Retrieving all posts from database
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts=cursor.fetchall()
#     # print(posts)
#     return {"data": posts}

# Creating post and storing it in database
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_Posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post= cursor.fetchone()
#     conn.commit()
    # return{"data": new_post}

# to retrieve a specific id from database with validation and its content with error handling
# @app.get("/posts/{id}")
# def get_post(id:int):
#     cursor.execute("""SELECT * FROM posts WHERE ID = %s """, (str(id)))
#     one_post=cursor.fetchone()
#     print(one_post)
#     if not one_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return {"post_detail": one_post}

# to delete a specific id from database with validation and its content with error handling
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):

#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
#     deleted_post=cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
#     return Response (status_code=status.HTTP_204_NO_CONTENT)

# to update a specific id from database with validation and its content with error handling
# @app.put("/posts/{id}")
# def update_post(id:int, post:Post):
#     cursor.execute("""UPDATE posts SET title= %s, content=%s, published=%s WHERE id= %s RETURNING * """, (post.title,post.content,post.published, str(id)))
#     updated_post=cursor.fetchone()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist") 
#     conn.commit()
#     return {"message":updated_post}
 
# --------------------------------------------------------------------
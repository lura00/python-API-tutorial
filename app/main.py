import enum
import psycopg2
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    # ratings: Optional[int] = None


# connect to database created in postgres
while True:

    try:
        conn = psycopg2.connect(host='localhost', database="fastapi", user='postgres',
                                password='solstad', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        # import time, this will make the while loop wait 2 secs before starting over.
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":
                                                                                    "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():

    return {"message": "Welcome to my API!!!!"}

# Show your posts from postgres database


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)""",
                   (post.title. post.content, post.published))
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    return {"data": "created post"}
# title string, content string, category, Boolean published or saved as draft


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}


@app.get("/posts/{id}")  # /{id} path parameter
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    print(post)
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array that has required id
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_dict = post.dict()  # convert post_dict to a dictionary
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}


# Original draft

# app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     ratings: Optional[int] = None


# @app.get("/")
# def root():

#     return {"message": "Welcome to my API!!!!"}


# @app.get("/posts")
# def get_posts():
#     return{"data": "This is your post"}


# @app.post("/createposts")
# def create_post(post: Post):
#     print(post)
#     print(post.dict())
#     return {"data": post}
# # title string, content string, category, Boolean published or saved as draft

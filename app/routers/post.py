# To clean the main-file we have made a new folder within out app-folder called routers.
# Here we have two files, user.py and post.py, in them all requests is stored and used via router.
# We have imported from fastAPI, APIrouter and set up a new keyword to connect to router, router = APIrouter().
# Then changed all @app. to @router.
# main now imports this files and set up a app.include_routers to include all routers within post and user.


from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
from typing import List

# This does so inte every path operation we dont need to put /posts. So if we have /posts/id we romove /posts since the prefix have already done that for us.
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Show your posts from postgres database

# Get all posts from my postgres DB table called "posts"


@router.get('/', response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Create a new post in postgres DB using SQL commands in python, %s = variable VALUE in this case post.tite etc.


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schema.Post)  # /{id} path parameter
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post in postgres DB using python commands

@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# title string, content string, category, Boolean published or saved as draft


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

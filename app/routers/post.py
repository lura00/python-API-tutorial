# To clean the main-file we have made a new folder within out app-folder called routers.
# Here we have two files, user.py and post.py, in them all requests is stored and used via router.
# We have imported from fastAPI, APIrouter and set up a new keyword to connect to router, router = APIrouter().
# Then changed all @app. to @router.
# main now imports this files and set up a app.include_routers to include all routers within post and user.


from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schema, oauth2
from ..database import get_db
from typing import List, Optional

# This does so inte every path operation we dont need to put /posts. So if we have /posts/id we romove /posts since the prefix have already done that for us.
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Show your posts from postgres database

# Get all posts from my postgres DB table called "posts"

# The last parameter in the function is the authorization to make sure user is logged in
# before he/she can do anything with any post.

# Add "limit: datatype" to def-parameter and add to query to get a limit to how many posts to get when "get all"
# In the qeury parameters, to skip a post, add skip to def-param and set a default.
# add "offset(skip)" to query-param. And to be able to search in the query.
# Add search to def param and set default to "Optional[str]" Also import Optional from Typing.
# Add to query, "filter(models.Post.title.contains(search)".


# @router.get('/', response_model=List[schema.Post])
@router.get('/', response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # to add id auth add ".filter(models.Post.owner_id == current_user.id).all()"
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

# Create a new post in postgres DB using SQL commands in python, %s = variable VALUE in this case post.tite etc.

# current_user comes from oauth2 function that return user using ID.

# To get the owner_id when we fetch a post, we need to add it to the schema we call for in the
# router.post, so to schema.py to see the changes.
# To not get an owner_id error when created a post we add owner_id=current_user.id
# to the new_post variable that contains the users dictionary


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schema.PostOut)  # /{id} path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    delete_post_query = db.query(models.Post).filter(models.Post.id == id)

    delete_post = delete_post_query.first()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    delete_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post in postgres DB using python commands

@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# title string, content string, category, Boolean published or saved as draft


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

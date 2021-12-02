# To clean the main-file we have made a new folder within out app-folder called routers.
# Here we have two files, user.py and post.py, in them all requests is stored and used via router.
# We have imported from fastAPI, APIrouter and set up a new keyword to connect to router, router = APIrouter().
# Then changed all @app. to @router.
# main now imports this files and set up a app.include_routers to include all routers within post and user.


from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db

# This does so inte every path operation we dont need to put /users. So if we have /users/id we romove /users since the prefix have already done that for us.
router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # Convert user to a dict and unpack ut (**)
    new_user = models.User(**user.dict())
    db.add(new_user)  # Adding to our db
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")

    return user

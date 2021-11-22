# Install SQLAlchemy
- pip install sqlalchemy in your terminal
- pip freeze if you want to see what packages you've installed

# Establish connection to your database
- Create a new file called database.py -->

# Import from SQLAlchemy lib
- from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    - This is what connecting to your postgres db will look like:
    SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-adress/hostname/hostname>/<database_name>'

# starting an engine
- If you are connecting to a SQLite db enter this info
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
- as well: connect_args={"check_same_thread": False in the ()

# Setting up a session

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class

    base = declarative_base()

# Creating a table using sqlAlchemy with python
- So now we are not using SQL code anymore, now we are passing python code that will be translatad to SQL
- Create a new py-file, lets call it models.py
- Here we will create our tables for our postgres db
- This is what you will be importing and how the code will typically look like:

    from sqlalchemy.sql.expression import null
    from .database import Base
    from sqlalchemy import Column, Integer, String, Boolean


    class Post(Base):
        __tablename__ = "posts"

        id = Column(Integer, primary_key=True, nullable=False)
        title = Column(String, nullable=False)
        content = Column(String, nullable=False)
        published = Column(Boolean, default=True)

# Setting up your sqlAlchemy with main-file
- import these in main.py:
    from sqlalchemy.orm import Session
    from . import models
    from .database import SessionLocal, engine
    from fastapi import Depends

- Copy this row. By running this line we create the tible within postgres
    models.Base.metadata.create_all(bind=engine) 

- Create a dependency:

    def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

- Create a function in main to test that it all works.

    @app.get("/posts")
    def test_posts(db: Session = Depends(get_db)):
    return {"Status": "Success"}

# Create a get-request using python and SQLaclhemy
    @app.get("/sqlalchemy")
    def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}

- We connect to our fastAPI with @app.
- define the functions name and add what we needs to be done in (). We call the get_db-function that lays
    in the database.py-file. scroll up one headline to see it.
- This function help us retrieve our table and data within.
- We create a query and send in what model we want to use. models that we design in models.py and we call
    the model using above models.Post).all(). We import models above as well in main.py.
- To get all, we add keyword (models.Post).all() there is more choices to be done. Using "all()" will just retrieve everything.

# Create a new post -request
    @ app.post("/posts", status_code=status.HTTP_201_CREATED)
    def create_post(post: Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

- Create function name add the data we need.
- create a variable that will represent our model in model.py (post).
    Use **post.dict() To make the model a dictionary and ** will unpack that for us.
    So if we add something to our model we do not need to change anything in the creat_post function.
- add the new variable to our db
- we need to commit like we do when writing SQL-code.
- db.refresh to see our update and the return as usual.
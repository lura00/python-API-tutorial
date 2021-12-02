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
- define the functions name and add the db as in the parameters. (Dependency)
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

- Connect to the API with @app.
- Create function name add the db in the parameters. (Dependency)
- create a variable that will represent our model in model.py (post).
    Use **post.dict() To make the model a dictionary and ** will unpack that for us.
    So if we add something to our model we do not need to change anything in the creat_post function.
- add the new variable to our db
- we need to commit like we do when writing SQL-code.
- db.refresh to see our update and the return as usual.

# Get on post with specific ID
    @app.get("/posts/{id}")  # /{id} path parameter
    def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": post}

- Connect to the API with @app.
- As usual we pass in the db as parameter in the function declaration. (Dependency)
- Then we do a query, filter in our model.Post for id, using dot"."id equals id. 
- Keyword "first()" to stop looking when the db has found the id.

# Delete one post
    @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_post(id: int, db: Session = Depends(get_db)):

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

- Connect to the API with @app.
- Add the db in the function declare parameters. (Dependency)
- Then do the query, connect to our model add the .post and .id to find the correct id
    you want to delete.
- If-statement same as in SQL-tutorial except one thing, the statement, delete_post.first()
    So the first post with id will be checked. 
- Then delete_post.delete() add the "sync_sess=False" to delete. That is default.
- Then when changes are to be made in the db table we have to commit, db.commit().

# Update a specific post
    @app.put("/posts/{id}")
    def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

- Connect to the API using @app.
- Add the db in the function declare parameters. (Dependency)
- Then do the query, connect to our model add the .post and .id to find the correct id
    you want to update.
- Set a varaible, "post" equals to post_query to save it.
- If-statement same as in SQL-tutorial except one thing, the statement, post == None
    So if the post doesn't excist we get  error 404.
- Then pass in post_qeury.updatge(updated_post.dict(), sync_sess=False) to update the dictionary.
    Set sync_sess to False, as per default.
- Then when changes are to be made in the db table we have to commit, db.commit().

# Create ORM-models in models.py
- Create models of how table should look like, what data we pass in must fit the mdoel.
- Here is a model for adding and creating users:

    class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

- Add what type then if nullable = False means that it can't be left blank. If keyword "unique" is added the same, in this example, email can't be entered more then once.

# Create new user and get-user (show profile)

    @ app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
    def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hash_password = utils.hash(user.password)
    user.password = hash_password
    # Convert user to a dict and unpack ut (**)
    new_user = models.User(**user.dict())
    db.add(new_user)  # Adding to our db
    db.commit()
    db.refresh(new_user)
    return new_user

- In our schema.py I have added a new schema, UserOut, wich I connect the @app to via response_model.
- We use "hash" to hash the password choosen by the user. Then no one will get or see the password.
- to use hash, install "pip install passlib[bcrypt], then import "from passlib.context import CryptContext"
    This is done in a seperate file called "Utils.py" where we will put all utilities for the program.

    @app.get('/users/{id}', response_model=schema.UserOut)
    def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user
    
- To get a profile I pass in id since every user has a specific id. 
- Here as well we connect to UserOut-schema. This means what info the user will get back.

# Path operation for login user (in new router, auth.py)

   @router.post('/login')
    def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

- import the new file oauth2.py from ".".
- import OAuth2PasswordRequestForm and set up and dependency, just like with the database.
- Set user_credentials to OAuth2PasswordRequestForm = Depends()
- in the db-queary set user_credentials.email to user_credentials.username.
- create the access token and return it.

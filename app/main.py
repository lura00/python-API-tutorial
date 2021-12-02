import psycopg2
import time
import sys
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from sqlalchemy.sql.functions import user
from . import models
from .database import engine
from .routers import post, user, auth

# By running this line we create the table within postgres

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
        # sys.exit(10)
        # import time, this will make the while loop wait 2 secs before starting over.
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":
                                                                                    "favorite foods", "content": "I like pizza", "id": 2}]

# Finding correct id for all the functions


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# Include our new folder router and the files in it. Then goes to the files and see if it can match router.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# Initializing fastAPI


@app.get("/")
def root():

    return {"message": "Welcome to my API!!!!"}

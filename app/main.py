from fastapi import FastAPI
from .routers import post, user, auth, vote
# Allows people from other domains talk to my API
from fastapi.middleware.cors import CORSMiddleware

# Youtube => 17:21:57
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# A function that goes through the request.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our new folder router and the files in it. Then goes to the files and see if it can match router.

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Initializing fastAPI


@app.get("/")
def root():

    return {"message": "Hello world, pushing out to ubuntu"}

from passlib.context import CryptContext

# import from passlib.context import Cryptocontext
# then define the settings for hash-password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

# Function that takes in a string password and compares to the hashed version and verifies it.


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

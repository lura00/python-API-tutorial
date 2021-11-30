from passlib.context import CryptContext

# import from passlib.context import Cryptocontext
# then define the settings for hash-password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

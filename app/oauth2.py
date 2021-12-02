from jose import JWTError, jwt
from datetime import datetime, timedelta

# Install this: pip install python-jose[cryptography]
# need the secret key
# Need algoritmhm that we are gonna use
# experation time of token.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pass in a dictionary with data. copy the data that is going to be encoded.
# Set up an expire-variable, import datetime and timedelta.
# update varibale "to_encode" with .update pass in the expire-varible.
# pass in the data in jwt.encode, see below, store it in a variable that will be returned.


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

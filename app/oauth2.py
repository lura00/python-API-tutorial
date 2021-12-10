from fastapi.param_functions import Depends
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Install this: pip install python-jose[cryptography]
# need the secret key
# Need algoritmhm that we are gonna use
# experation time of token.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Pass in a dictionary with data. copy the data that is going to be encoded.
# Set up an expire-variable, import datetime and timedelta.
# update varibale "to_encode" with .update pass in the expire-varible.
# pass in the data in jwt.encode, see below, store it in a variable that will be returned.

# Sets the parameters for the access token, expire time, takes the token to encode
# Store the encoded token and returns it.


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# verifies the token, stor decoded token i variable, payload.
# extract id from payload
# gets user_id and if no errors occur returns token_data.
# Since token_data stores the TokenData schema it only stores id, for now.


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

# Gets the user that is logging in from post.py and verify all operations  that will commit something
# before the commit goes through.
# Make sure the Token_data and token matches our set schemas
# return error will occur if credentials is wrong
# if all data is correct nothing will be returned.


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

    # In this function we get the user from ID and returning it. So whatever returns from here
    # Will show printing when I call this from my post.py or whatever.

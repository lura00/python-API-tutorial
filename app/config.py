from pydantic import BaseSettings
# Environment variables called to by schema below.
# All environment variables is created in ".env-file" That should always be secret and not posted
# ex. Github.


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


# Creating an instance of class Settings
settings = Settings()

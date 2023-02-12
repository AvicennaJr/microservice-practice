from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configure environmental variables"""

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    API_SECRET: str
    ALGORITHM: str
    TOKEN_EXPIRY: int

    class Config:
        env_file = ".env"


settings = Settings()

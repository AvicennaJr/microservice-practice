from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configure environmental variables"""

    # postgres database variables
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "users"

    # postgres test database variables
    TEST_DATABASE_USERNAME: str = "postgres"
    TEST_DATABASE_PASSWORD: str = "postgres"
    TEST_DATABASE_HOST: str = "localhost"
    TEST_DATABASE_PORT: str = "5432"
    TEST_DATABASE_NAME: str = "users_test"

    # JWT token variables
    API_SECRET: str
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRY: int = "60"

    class Config:
        env_file = ".env"


settings = Settings()

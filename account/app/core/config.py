from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configure environmental variables"""

    # postgres database variables
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "accounting"

    # postgres test database variables
    TEST_DATABASE_USERNAME: str = "postgres"
    TEST_DATABASE_PASSWORD: str = "postgres"
    TEST_DATABASE_HOST: str = "localhost"
    TEST_DATABASE_PORT: str = "5432"
    TEST_DATABASE_NAME: str = "accounting_test"

    # rabbitmq variables
    RABBITMQ_URL: str

    class Config:
        env_file = ".env"


settings = Settings()

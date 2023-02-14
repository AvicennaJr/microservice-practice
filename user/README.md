# USER MICROSERVICE
## Setup
### Clone the repository
Clone the repository with:
```
git clone https://gitlab.com/JustFuad/savings-scheme
```
Then enter the `user` folder with:
```
cd savings-scheme/user/
```
### Install requirements
Install the dependencies with:
```
pip install -r requirements.txt
```
### Fill in the environmental variables
- Rename the `.env_example` file to `.env` and fill the following parameters:
    - Postgres database variables:
        - `DATABASE_USERNAME`: The username of your database. The default is `postgres`.
        - `DATABASE_PASSWORD`: The password of your database user. The default is `postgres`.
        - `DATABASE_HOST`: The host of your database. The default is `localhost`.
        - `DATABASE_PORT`: The port of your database. The default is `5432`.
        - `DATABASE_NAME`: The name of your database. The default is `user`.
    - Postgres test database variables:
        - `TEST_DATABASE_USERNAME`: The username of your test database. The default is `postgres`.
        - `TEST_DATABASE_PASSWORD`: The password of your test database user. The default is `postgres`.
        - `TEST_DATABASE_HOST`: The host of your test database. The default is `localhost`.
        - `TEST_DATABASE_PORT`: The port of your test database. The default is `5432`.
        - `TEST_DATABASE_NAME`: The name of your database. The default is `user`.
    - JWT token variables:
        - `API_SECRET`: A random secret key that will be used to sign the JWT tokens. You can generate a random key with:
        ```
        openssl rand -hex 32
        ```
        - `ALGORITHM`: Algorithm used to sign the JWT token. The default is `HS256`.
        - `TOKEN_EXPIRY`: Number of minutes a token will be valid. The default is 60 minutes.
## Running the app
You can run the app and test the endpoints with:
```
uvicorn app.api.main:app --reload
```
## API Documentation
You can find the API docs at http://127.0.0.1:8000/docs
## Running tests
You can run tests with:
```
pytest -v
```
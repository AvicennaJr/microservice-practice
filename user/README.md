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
### Requirements
- Python 3.9
- PostgreSQL v13+
- Docker v23.0.1+
- Docker Compose v2.16.0+

### Dependencies
Install the python dependencies with:
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
    - Docker variables:
        - `APPLICATION_PORT`: Port where the host machine will run the application.
        - `DATABASE_DEVELOPMENT_PORT`: Port where the host machine will connect to the database container.
        - `DATABASE_TESTING_PORT`: Port where host machine will connect to the test database container.
    - RabbitMQ variables:
        - `RABBITMQ_URL`: The RabbitMQ url connect to in the format:
        ```
        scheme://username:password@host:port/virtual_host
        ```
        The scheme can be `amqp` for non SSL connections and `amqps` for SSL connections.
        - `HEARTBEAT`: Pass a value greater than zero to enable heartbeats between the server and the application. The integer passed will be the number of seconds between heartbeats. The default is 300 seconds.
        - `CONNECTION_ATTEMPTS`: The number of connection attempts after a failed connection. The default is 10 attempts.
        - `RETRY_DELAY`: The number of seconds to wait before attempting to reconnect a failed connection. The default wait time is 60 seconds.
## Running the app
### Locally
- Fill in the environmental variables according
- Run the app with:
```
uvicorn app.api.main:app --reload
```
### With Docker
- Fill in the environmental variables
- Build the containers with:
```
docker compose build
```
- Run the application with:
```
docker compose up
```
## API Documentation
You can find the API docs at http://127.0.0.1:8000/docs
## Running tests
### Locally
- You can run tests locally with:
```
pytest -v
```
### With Docker
- Access the containers shell with:
```
docker compose exec backend sh
```
- Run tests with:
```
pytest -v
```
# Services

This directory contains three microservices and one external PostgreSQL service.

## Structure

- `auth-service/` — FastAPI service for user registration and authentication.
- `user-service/` — FastAPI service for user management with SQLAlchemy and PostgreSQL.
- `order-service/` — FastAPI service for order management.
- `docker-compose.yml` — Docker Compose configuration to run all services.
- `docker-compose-secrets.env` — secrets for PostgreSQL connection.

## Technologies

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy (in `user-service`)
- PostgreSQL
- Docker, Docker Compose

## How to run

From the `services` root directory, run:

```bash
docker compose up -d --build
```

Or from the repository root:

```bash
cd services
docker compose up -d --build
```

To stop the services:

```bash
docker compose down
```

## Services and ports

- `auth-service` — `http://localhost:8000`
- `user-service` — `http://localhost:8001`
- `order-service` — `http://localhost:8002`
- `postgres` — port `5432`

## Main endpoints

### auth-service

- `POST /register` — register a new user
- `POST /login` — login and get a JWT

### user-service

- `GET /` — health check
- `POST /users` — create a user
- `GET /users/{user_id}` — get user by ID
- `GET /users` — list users

### order-service

- `GET /` — health check
- `POST /orders` — create an order
- `GET /orders/{order_id}` — get order by ID
- `GET /orders` — list orders

## Notes

- `auth-service` and `order-service` store data in memory, so data is lost after container restart.
- `user-service` persists users in the PostgreSQL database.

## Requirements

- Docker
- Docker Compose

## Useful commands

```bash
docker compose ps

docker compose logs auth-service

docker compose logs user-service

docker compose logs order-service

docker compose logs postgres
```

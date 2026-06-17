# DevOps Cloud Platform

This project simulates a real-world cloud-native microservices system using:
- Auth Service (authentication)
- User Service (user management)
- Order Service (orders)

## Architecture
Auth Service
    │
    ▼
User Service
    │
    ▼
PostgreSQL

Order Service

## Services
- Auth Service
- User Service
- Order Service
- PostgreSQL

## Stack
- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose

## Run
git clone [<repo>](https://github.com/dbatula/DevOps-Platform.git)
git clone https://github.com/dbatula/DevOps-Platform.git

cd services

docker compose up -d

## Endpoints
Auth Service
http://localhost:8000/docs

User Service
http://localhost:8001/docs

Order Service
http://localhost:8002/docs
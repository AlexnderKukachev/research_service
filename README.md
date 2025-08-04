
# Clinical Sample Management Microservice

## 🧪 Project Description

This service is a backend microservice designed to manage biological samples collected in clinical trials. It was developed as part of a technical challenge for the Backend Engineer position.

The microservice supports operations such as creating, reading, filtering, authentication, and storage of samples, with a focus on scalability and future integration with AI agents and analytical systems.

---

## 🚀 Technologies

- **Python 3.11**
- **FastAPI** — lightweight and fast framework for building REST APIs
- **MongoDB** — for storing biological samples (flexibility and scalability)
- **PostgreSQL (asyncpg)** — for storing user data (ACID compliance, normalization)
- **SQLAlchemy Async ORM**
- **Docker / docker-compose** — environment isolation and ease of launch
- **Pytest + httpx + aiosqlite** — unit and integration testing
- **Pydantic** — validation and serialization

---

## 📦 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/AlexnderKukachev/research_service.git
cd research_service
```

### 2. Create `.env` file based on example

```bash
cp .env.example .env
```
For local setup set the next variable like follow:
MONGODB_URI=mongodb://mongo:27017
POSTGRES_URI=postgresql+asyncpg://postgres:postgres@postgres/research_users
DB_NAME=research_db

### 3. Run the service

```bash
docker-compose up --build
```

API will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ Authentication

To access protected routes:

```http
POST /token
Body: form-data
  - username: <username>
  - password: <password>
```

Response:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

Add token to the header:

```
Authorization: Bearer <access_token>
```

---

## 🧪 Testing

```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build
```

Or manually:

```bash
docker-compose run app pytest
```

---

## 📁 Project Structure

```
research_service/
├── auth.py            # Authentication and tokens
├── crud.py            # Business logic for DB access
├── database.py        # PostgreSQL and MongoDB setup
├── main.py            # Entrypoint + route handlers
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic schemas
├── config.py          # .env configuration
└── tests/             # Unit and integration tests
```

---

## 🧠 Completed Features

- [x] CRUD operations for samples: create, read, filter, update, delete
- [x] JWT-based authentication
- [x] Input data validation
- [x] Dockerfile + docker-compose support
- [x] Logging
- [x] Async access to PostgreSQL and MongoDB
- [x] Unit and integration test coverage
- [x] Action logging

---

## ⚠️ What Could Be Improved with More Time

- [ ] Add database migrations (e.g., Alembic)
- [ ] Implement caching (Redis)
- [ ] Define user roles (e.g., admin, technical)
- [ ] Add observability tools (OpenTelemetry, Prometheus)
- [ ] Persist logs to file or external service (ELK, Sentry)

---

## ⚖️ Trade-offs

- MongoDB was chosen for storing samples due to its flexible and schema-less nature.
- PostgreSQL was used for user data due to strict schema needs and ease of implementing secure authentication.
- Alembic migrations were skipped to save time (4-hour limit).
- No frontend was implemented — the service is intended to be integrated with UI or AI agents later.

---

## 🤖 AI Usage

The service was partially developed using **ChatGPT 4.0** as a code generation and productivity tool. All architectural and technical decisions were made manually.

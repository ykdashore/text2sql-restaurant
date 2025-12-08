# Text-to-SQL Query Engine

A production-ready FastAPI service that converts natural language questions into SQL queries.  
It includes a safe SQL executor, schema-aware validation, Dockerized environment, and a complete test suite running through Docker Compose.

---

## Features

- Convert plain English questions into SQL queries  
- Validate SQL for safety (blocks DROP/DELETE/TRUNCATE, etc.)  
- Execute queries against a PostgreSQL database  
- Expose a clean API using FastAPI  
- Fully containerized (`app`, `db`, `tests`)  
- Unit tests run inside Docker  
- Supports integration with Gemini (via `langchain-google-genai`)


---

## Tech Stack

- FastAPI  
- PostgreSQL  
- LangChain + Gemini API  
- psycopg2  
- Docker + Docker Compose  
- Pytest + httpx


## Setup


1. Environment Variables

### 1. Environment Variables

Create a .env file:

POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
POSTGRES_DB=restaurantdb\
GEMINI_API_KEY=your-key-here\
API_KEYS=test-key-123,test-key-456\
TESTING_KEY=test-key-123

---

## Run the Project

### Start the app + database

docker-compose up --build

--- 

API will be available at:

http://localhost:8010


Swagger docs:

http://localhost:8010/docs

Run Tests

Tests execute inside the Docker Compose environment:

docker-compose run --rm tests

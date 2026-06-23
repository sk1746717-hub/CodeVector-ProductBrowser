# CodeVector Product Browser

Backend assignment built using FastAPI and PostgreSQL.

## Features

* 200,000 generated products
* Category filtering
* Cursor pagination
* PostgreSQL database
* FastAPI backend
* Swagger API documentation

## Run

```bash
python -m uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000/docs

## Database

PostgreSQL 17

## Pagination

Cursor-based pagination using created_at and id to avoid duplicates and missing records while data changes.

## Seed Data

```bash
python seed.py
```

Generates 200,000 products.

# FastAPI CRUD API with PostgreSQL

## Overview

This project is a REST API built using FastAPI and PostgreSQL. It implements basic CRUD operations with proper request validation and structured responses.

## Tech Stack

- Python 3.x
- FastAPI
- PostgreSQL
- SQLAlchemy
- Uvicorn

## Features

- Create new records
- Retrieve single or multiple records
- Update existing records
- Delete records
- Input validation using Pydantic
- Proper HTTP status codes

## What I Learned

- Designing database schemas before writing API logic
- Structuring backend code into routers, models, schemas
- Managing DB sessions properly
- Understanding request lifecycle
- Error handling in REST APIs

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

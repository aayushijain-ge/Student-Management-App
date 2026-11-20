# Student Management API

A backend project built using **FastAPI** to learn backend development through practical implementation.


# Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Git & GitHub

---


#  Day 1 - Backend Fundamentals & Web API Basics

## Topics Covered

- Frontend vs Backend
- Client-Server Architecture
- HTTP Request & Response
- HTTP Methods
- HTTP Status Codes
- REST API Fundamentals
- JSON Response
- FastAPI Basics
- Swagger API Documentation

---


# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome API |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| POST | `/students` | Add a new student |
| PUT | `/students/{student_id}` | Update an existing student |
| DELETE | `/students/{student_id}` | Delete a student |

---

# Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/aayushijain-ge/Student-Management-App.git
```

## 2. Navigate to the Project

```bash
cd Backend
```

## 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

## 4. Activate the Virtual Environment

```bash
source venv/bin/activate
```
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 6. Start the FastAPI Server

```bash

python -m uvicorn app.main:app --reload
```

---

#  API Documentation

To run the server, open: http://127.0.0.1:8000/

For Swagger UI

```text
http://127.0.0.1:8000/docs
```
```
To run : Celery worker
celery -A app.core.celery_app.celery_app worker --loglevel=info
---
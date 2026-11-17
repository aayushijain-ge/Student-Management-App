# Student Management API

A backend project built using **FastAPI** to learn backend development through practical implementation.
---

# Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Git & GitHub

---

#  Project Structure (Day 1)

```text
Student-Management-App/
│
├── venv/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

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

## Features Implemented

- Welcome API
- Get All Students
- Get Student by ID
- Add New Student
- Update Student
- Delete Student

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

# How to Run the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
```

## 2. Navigate to the Project

```bash
cd Student-Management-App
```

## 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

## 4. Activate the Virtual Environment

### Ubuntu/Linux

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
python -m uvicorn main:app --reload
```

---

# 📖 API Documentation

After running the server, open: http://127.0.0.1:8000/

For Swagger UI

```text
http://127.0.0.1:8000/docs
```
```

---
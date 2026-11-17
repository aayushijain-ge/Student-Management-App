from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Student Management API",
    description="Day 1 - FastAPI CRUD Implementation",
    version="1.0.0"
)


# -------------------------
# Pydantic Model
# -------------------------

class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str


# -------------------------
# Temporary Database
# -------------------------

students = [
    {
        "id": 1,
        "name": "Aayushi",
        "age": 22,
        "course": "Python"
    },
    {
        "id": 2,
        "name": "Rahul",
        "age": 21,
        "course": "Java"
    }
]


# -------------------------
# Home Route
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API"
    }


# -------------------------
# Get All Students
# -------------------------

@app.get("/students", status_code=status.HTTP_200_OK)
def get_students():
    return students


# -------------------------
# Get Student By ID
# -------------------------

@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# -------------------------
# Add Student
# -------------------------

@app.post("/students", status_code=status.HTTP_201_CREATED)
def add_student(student: Student):

    for s in students:
        if s["id"] == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    students.append(student.model_dump())

    return {
        "message": "Student added successfully",
        "student": student
    }


# -------------------------
# Update Student
# -------------------------

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            students[index] = updated_student.model_dump()

            return {
                "message": "Student updated successfully",
                "student": updated_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# -------------------------
# Delete Student
# -------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
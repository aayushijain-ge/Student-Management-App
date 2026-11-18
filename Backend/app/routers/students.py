from fastapi import APIRouter, HTTPException, status

from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services import student_service

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=list[StudentResponse])
def get_students():
    return student_service.get_all_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def add_student(data: StudentCreate):
    return student_service.create_student(data)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentUpdate):
    student = student_service.update_student(student_id, data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int):
    if not student_service.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
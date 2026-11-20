from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.services import student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def add_student(data: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, data)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not student_service.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
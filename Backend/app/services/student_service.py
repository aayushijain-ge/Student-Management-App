from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def get_all_students(db: Session):
    return db.scalars(select(Student)).all()


def get_student_by_id(db: Session, student_id: int):
    return db.get(Student, student_id)


def create_student(db: Session, data: StudentCreate):
    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student_id: int, data: StudentUpdate):
    student = db.get(Student, student_id)
    if not student:
        return None
    for field, value in data.model_dump().items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> bool:
    student = db.get(Student, student_id)
    if not student:
        return False
    db.delete(student)
    db.commit()
    return True
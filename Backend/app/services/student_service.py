from app.db.fake_db import students_db
from app.schemas.student import StudentCreate, StudentUpdate


def get_all_students():
    return students_db


def get_student_by_id(student_id: int):
    for student in students_db:
        if student["id"] == student_id:
            return student
    return None


def create_student(data: StudentCreate):
    new_id = max((s["id"] for s in students_db), default=0) + 1
    student = {"id": new_id, **data.model_dump()}
    students_db.append(student)
    return student


def update_student(student_id: int, data: StudentUpdate):
    for index, student in enumerate(students_db):
        if student["id"] == student_id:
            students_db[index] = {"id": student_id, **data.model_dump()}
            return students_db[index]
    return None


def delete_student(student_id: int) -> bool:
    student = get_student_by_id(student_id)
    if student:
        students_db.remove(student)
        return True
    return False
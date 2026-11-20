from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

from app.core import cache
from app.schemas.student import StudentResponse


# def get_all_students(
#     db: Session,
#     search: str | None = None,
#     course: str | None = None,
#     skip: int = 0,
#     limit: int = 10,
# ):
#     query = select(Student)

#     if course:
#         query = query.where(Student.course == course)
#     if search:
#         query = query.where(Student.name.ilike(f"%{search}%"))

#     total = db.scalar(select(func.count()).select_from(query.subquery()))

#     items = db.scalars(
#         query.order_by(Student.id).offset(skip).limit(limit)
#     ).all()

#     return {"total": total, "skip": skip, "limit": limit, "items": items}

##Caching


def get_all_students(
    db: Session,
    search: str | None = None,
    course: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    key = f"students:search={search}:course={course}:skip={skip}:limit={limit}"

    cached = cache.get(key)
    if cached is not None:
        print("CACHE HIT ", key)
        return cached

    print("CACHE MISS", key)

    query = select(Student)
    if course:
        query = query.where(Student.course == course)
    if search:
        query = query.where(Student.name.ilike(f"%{search}%"))

    total = db.scalar(select(func.count()).select_from(query.subquery()))
    rows = db.scalars(query.order_by(Student.id).offset(skip).limit(limit)).all()

    # convert DB objects to plain dicts before caching
    items = [StudentResponse.model_validate(r).model_dump() for r in rows]

    result = {"total": total, "skip": skip, "limit": limit, "items": items}
    cache.set(key, result, ttl=60)
    return result



def get_student_by_id(db: Session, student_id: int):
    return db.get(Student, student_id)


# def create_student(db: Session, data: StudentCreate):
#     student = Student(**data.model_dump())
#     db.add(student)
#     db.commit()
#     db.refresh(student)
#     return student

def create_students_bulk(db: Session, items: list[StudentCreate]):
    students = [Student(**item.model_dump()) for item in items]
    db.add_all(students)
    db.commit()
    cache.clear_prefix("students:")  
    for s in students:
        db.refresh(s)
    return students


def update_student(db: Session, student_id: int, data: StudentUpdate):
    student = db.get(Student, student_id)
    if not student:
        return None
    for field, value in data.model_dump().items():
        setattr(student, field, value)
    db.commit()
    cache.clear_prefix("students:")  
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> bool:
    student = db.get(Student, student_id)
    if not student:
        return False
    db.delete(student)
    db.commit()
    cache.clear_prefix("students:")  
    return True
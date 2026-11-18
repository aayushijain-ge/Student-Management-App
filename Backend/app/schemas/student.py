from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    age: int
    course: str


class StudentCreate(StudentBase):
    pass           

class StudentUpdate(StudentBase):
    pass       


class StudentResponse(StudentBase):
    id: int         # what the API sends back
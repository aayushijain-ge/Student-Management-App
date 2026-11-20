from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    name: str
    age: int
    course: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StudentListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[StudentResponse]
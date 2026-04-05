from pydantic import BaseModel, ConfigDict

class ToDoRequest(BaseModel):
    name: str
    completed: bool

class ToDoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    completed: bool
    id: int

    # class Config:
    #     orm_mode = True

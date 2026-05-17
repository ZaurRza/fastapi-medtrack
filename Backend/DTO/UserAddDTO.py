from pydantic import BaseModel
#DTO для добавления пользователя
class UserAdd(BaseModel):
    password: str
    worker_number: int
    role: str
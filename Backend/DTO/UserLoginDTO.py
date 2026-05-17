from pydantic import BaseModel
#DTO для логина пользователя
class UserLogin(BaseModel):
    worker_number: int
    password: str
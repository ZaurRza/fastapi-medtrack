from pydantic import BaseModel
#DTO для выхода пользователя из аккаунта
class UserLogout(BaseModel):
    worker_number: int

from pydantic import BaseModel
#DTO для добавления фармацевта
class PharmacistAdd(BaseModel):
    name: str
    worker_number: int
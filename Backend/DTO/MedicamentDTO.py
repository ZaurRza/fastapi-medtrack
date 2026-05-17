from pydantic import BaseModel
#DTO для создания медикамента
class MedicamentCreate(BaseModel):
    unical_number: int
    name: str
    price: float
    production_date: str
    expiration_date: str
    production_country: str
    type: str
    recipe_needed: bool

class MedicamentChange(BaseModel):
    name: str
    price: float
    production_date: str
    expiration_date: str
    production_country: str
    type: str
    recipe_needed: bool
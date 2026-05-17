from pydantic import BaseModel
#DTO для продажи медикамента
class SaleMedicament(BaseModel):
    worker_number: int
    unical_number: int
    person: str
class SaleRecipe(BaseModel):
    worker_number: int
    recipe_number: int
    person: str
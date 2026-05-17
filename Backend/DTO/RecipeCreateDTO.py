from typing import List
from pydantic import BaseModel
#DTO для создания рецепта
class RecipeCreate(BaseModel):
    recipe_number: int
    organization: str
    doctor: str
    patient: str
    recipe_date: str
    medicament_list: List[int]
    
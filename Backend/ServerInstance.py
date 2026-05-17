from fastapi import FastAPI,HTTPException
from DTO.RecipeCreateDTO import RecipeCreate
from DTO.PharmacistAddDTO import PharmacistAdd
from DTO.UserAddDTO import UserAdd
from DTO.UserLoginDTO import UserLogin
from DTO.UserLogoutDTO import UserLogout
from DTO.MedicamentDTO import MedicamentCreate
from DTO.MedicamentDTO import MedicamentChange
from DTO.SaleDTO import SaleMedicament
from DTO.SaleDTO import SaleRecipe
import API.InventoryAPI as InventoryAPI
import API.RecipeAPI as RecipeAPI
import API.SaleAPI as SaleAPI
import API.PharmacistAPI as PharmacistAPI
import API.UsersAPI as UserAPI
import API.MedicamentAPI as MedicamentAPI
app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "MedTrack API is running"
    }

#Функция для обработки ошибок в API
def validate_res(res):
    if res[0]=="ERR":
        raise HTTPException(status_code=res[1],detail=res[2])
        return {}
    return res[3]

#API Инвентаря
inventory_api=InventoryAPI.InventoryAPI()
@app.get("/inventory/display")
def display_inventory():
    res=inventory_api.display_inventory()
    return validate_res(res)

@app.post("/inventory/add")
def add_to_inventory(unical_number:int):
    res=inventory_api.add_to_inventory(unical_number)
    return validate_res(res)

#API Рецептов
recipe_api=RecipeAPI.RecipeAPI()
@app.get("/recipe/display")
def display_recipe():
    res=recipe_api.display_recipe()
    return validate_res(res)

@app.get("/recipe/display/{recipe_number}")
def display_recipe_by_num(recipe_number:int):
    res=recipe_api.display_recipe_by_num(recipe_number)
    return validate_res(res)

@app.post("/recipe/add")
def add_recipe(recipe_data: RecipeCreate):
    res=recipe_api.add_recipe(recipe_data.recipe_number,
        recipe_data.organization,
        recipe_data.doctor,
        recipe_data.patient,
        recipe_data.recipe_date,
        recipe_data.medicament_list)
    return validate_res(res)

@app.delete("/recipe/delete/{recipe_number}")
def delete_recipe(recipe_number:int):
    res=recipe_api.delete_recipe(recipe_number)
    return validate_res(res)

#API Фармацевтов
pharmacist_api=PharmacistAPI.PharmacistAPI()
@app.get("/pharmacist/display")
def display_pharmacist():
    res=pharmacist_api.display_pharmacist()
    return validate_res(res)

@app.post("/pharmacist/add")
def add_pharmacist(pharmacist_data: PharmacistAdd):
    res=pharmacist_api.add_pharmacist(pharmacist_data.name, pharmacist_data.worker_number)
    return validate_res(res)

@app.delete("/pharmacist/delete/{worker_number}")
def delete_pharmacist(worker_number:int):
    res=pharmacist_api.delete_pharmacist(worker_number)
    return validate_res(res)

#API Пользователей
user_api=UserAPI.UsersAPI()
@app.get("/user/display")
def display_user():
    res=user_api.display_users()
    return validate_res(res)

@app.post("/user/add")
def add_user(user_data: UserAdd):
    res=user_api.add_user(user_data.password, user_data.worker_number, user_data.role)
    return validate_res(res)

@app.delete("/user/delete/{worker_number}")
def delete_user(worker_number:int):
    res=user_api.delete_user(worker_number)
    return validate_res(res)

@app.post("/user/login")
def login_user(user_data: UserLogin):
    res=user_api.login_user(user_data.worker_number,user_data.password)
    return validate_res(res)

@app.post("/user/mobile_login")
def mobile_login_user(user_data: UserLogin):
    res=user_api.mobile_login_user(user_data.worker_number,user_data.password)
    return validate_res(res)

@app.post("/user/logout")
def logout_user(user_data: UserLogout):
    res=user_api.logout_user(user_data.worker_number)
    return validate_res(res)

@app.get("/user/check_session/{worker_number}")
def check_session(worker_number:int):
    res=user_api.check_session(worker_number)
    return validate_res(res)

#API Медикаментов
medicament_api=MedicamentAPI.MedicamentAPI()
@app.get("/medicament/display")
def display_medicament():
    res=medicament_api.display_medicament()
    return validate_res(res)

@app.post("/medicament/add")
def add_medicament(medicament_data: MedicamentCreate):
    res=medicament_api.add_medicament(medicament_data.name, medicament_data.price, medicament_data.unical_number, medicament_data.production_date, medicament_data.expiration_date, medicament_data.production_country, medicament_data.type, medicament_data.recipe_needed)
    return validate_res(res)

@app.delete("/medicament/delete/{unical_number}")
def delete_medicament(unical_number:int):
    res=medicament_api.delete_medicament(unical_number)
    return validate_res(res)

@app.get("/medicament/display/{unical_number}")
def display_medicament_exact(unical_number:int):
    res=medicament_api.display_medicament_exact(unical_number)
    return validate_res(res)

@app.put("/medicament/change/{unical_number}")
def change_medicament(unical_number:int, medicament_data: MedicamentChange):
    res=medicament_api.change_medicament(medicament_data.name, medicament_data.price, unical_number, medicament_data.production_date, medicament_data.expiration_date, medicament_data.production_country, medicament_data.type, medicament_data.recipe_needed)
    return validate_res(res)

#API Продаж
sale_api=SaleAPI.SaleAPI()
@app.get("/sale/display")
def display_sale():
    res=sale_api.display_sale()
    return validate_res(res)

@app.get("/sale/display/recipe/{recipe_number}")
def display_sale_by_recipe(recipe_number:int):
    res=sale_api.display_sale_by_recipe(recipe_number)
    return validate_res(res)

@app.get("/sale/display/medicament/{unical_number}")
def display_sale_by_medicament(unical_number:int):
    res=sale_api.display_sale_by_medicament(unical_number)
    return validate_res(res)

@app.get("/sale/display/pharmacist/{worker_number}")
def display_sale_by_pharmacist(worker_number:int):
    res=sale_api.display_sale_by_pharmacist(worker_number)
    return validate_res(res)

@app.post("/sale/add/medicament")
def add_sale_only_medicament(sale_data: SaleMedicament):
    res=sale_api.add_sale_only_medicament(sale_data.unical_number, sale_data.worker_number, sale_data.person)
    return validate_res(res)

@app.post("/sale/add/recipe")
def add_sale_only_recipe(sale_data: SaleRecipe):
    res=sale_api.add_sale_only_recipe(sale_data.recipe_number, sale_data.worker_number, sale_data.person)
    return validate_res(res)

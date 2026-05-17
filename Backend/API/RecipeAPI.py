import Controller.RecipeController as RecipeController
class RecipeAPI(object):
    """Класс для валидации входных данных и реализации API рецептов"""
    def __init__(self):
        self._controller=RecipeController.RecipeController()
#Валидация данных
    def _recipe_number_validate(self,recipe_number):
        if recipe_number is None:
            return ("ERR",400,"Номер рецепта не может быть пустым!")
        
        if recipe_number<=0:
            return ("ERR",400,"Номер рецепта должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    
    def _add_recipe_validate(self,recipe_number,organization,doctor,patient,recipe_date,medicament_list):
        validation_result=self._recipe_number_validate(recipe_number)
        if validation_result[0]=="ERR":
            return validation_result
        
        if organization is None or doctor is None or patient is None or recipe_date is None or medicament_list is None:
            return ("ERR",400,"Все поля должны быть заполнены!")
        
        for medicament in medicament_list:
            if medicament<=0:
                return ("ERR",400,"Номера медикаментов должны быть положительными числами!")
            
        return ("OK",200,"Валидация прошла успешно!")
    
#Реализация API
    def display_recipe(self):
        result=self._controller.display_all()
        return result
    
    def display_recipe_by_num(self,recipe_number):
        validation_result=self._recipe_number_validate(recipe_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.display_recipe_exact(recipe_number)
        return result
    
    def add_recipe(self,recipe_number,organization,doctor,patient,recipe_date,medicament_list):
        validation_result=self._add_recipe_validate(recipe_number,organization,doctor,patient,recipe_date,medicament_list)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.add_recipe(recipe_number,organization,doctor,patient,recipe_date,medicament_list)
        return result
    
    def delete_recipe(self,recipe_number):
        validation_result=self._recipe_number_validate(recipe_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.delete_recipe(recipe_number)
        return result
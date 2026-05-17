import Controller.MedicamentController as MedicamentController
import time as time
class MedicamentAPI(object):
    """Класс для валидации входных данных и реализации API медикаментов"""
    def __init__(self):
        self._controller=MedicamentController.MedicamentController()
#Валидация данных
    def _unical_number_validate(self,unical_number):
        if unical_number is None:
            return ("ERR",400,"Серийный номер не может быть пустым!")
        
        if unical_number<=0:
            return ("ERR",400,"Серийный номер должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    
    def _medicament_validate(self,name,price,production_date,expiration_date,production_country,type,recipe_needed):
        time_format="%Y-%m-%d"

        if name is None or name.strip()=="":
            return ("ERR",400,"Название медикамента не может быть пустым!")
        if price is None or price<=0:
            return ("ERR",400,"Цена должна быть положительным числом!")
        if production_date is None:
            return ("ERR",400,"Дата производства не может быть пустой!")
        if expiration_date is None:
            return ("ERR",400,"Дата истечения срока годности не может быть пустой!")
        try:
            expiration=time.strptime(expiration_date,time_format)
        except ValueError:
            return ("ERR",400,"Дата истечения срока годности должна быть в формате YYYY-MM-DD!")
        try:
            production=time.strptime(production_date,time_format)
        except ValueError:
            return ("ERR",400,"Дата производства должна быть в формате YYYY-MM-DD!")
        if expiration<=production:
            return ("ERR",400,"Дата истечения срока годности должна быть позже даты производства!")
        if production_country is None or production_country.strip()=="":
            return ("ERR",400,"Страна производства не может быть пустой!")
        if type is None or type.strip()=="":
            return ("ERR",400,"Тип медикамента не может быть пустым!")
        if recipe_needed is None:
            return ("ERR",400,"Признак необходимости рецепта не может быть пустым!")
        return ("OK",200,"Валидация прошла успешно!")
#Реализация API
    def display_medicament(self):
        result=self._controller.display_all()
        return result
    
    def add_medicament(self,name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed):
        validation_result=self._unical_number_validate(unical_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._medicament_validate(name,price,production_date,expiration_date,production_country,type,recipe_needed)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.add_medicament(name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed)
        return result
    
    def delete_medicament(self,unical_number):
        validation_result=self._unical_number_validate(unical_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.delete_medicament(unical_number)
        return result
    
    def display_medicament_exact(self,unical_number):
        validation_result=self._unical_number_validate(unical_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.display_medicament_exact(unical_number)
        return result
    
    def change_medicament(self,name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed):
        validation_result=self._unical_number_validate(unical_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._medicament_validate(name,price,production_date,expiration_date,production_country,type,recipe_needed)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.change_medicament(name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed)
        return result
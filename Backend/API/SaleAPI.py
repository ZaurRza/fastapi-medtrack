import Controller.SaleController as SaleController
class SaleAPI(object):
    """Класс для валидации входных данных и реализации API продаж"""
    def __init__(self):
        self._controller=SaleController.SaleController()

#Валидация данных
    def _worker_number_validate(self,worker_number):
        if worker_number is None:
            return ("ERR",400,"Номер работника не может быть пустым!")
        
        if worker_number<=0:
            return ("ERR",400,"Номер работника должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    def _recipe_validate(self,recipe_number):
        if recipe_number is None:
            return ("ERR",400,"Номер рецепта не может быть пустым!")
        
        if recipe_number<=0:
            return ("ERR",400,"Номер рецепта должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    def _medicament_validate(self,unical_number):
        if unical_number is None:
            return ("ERR",400,"Уникальный номер медикамента не может быть пустым!")
        
        if unical_number<=0:
            return ("ERR",400,"Уникальный номер медикамента должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    def _person_validate(self,person):
        if person is None or person.strip()=="":
            return ("ERR",400,"Имя покупателя не может быть пустым!")
        
        return ("OK",200,"Валидация прошла успешно!")
#Реализация API
    #Реализация API для продажи медикамента без рецепта
    def display_sale(self):
        result=self._controller.display_all()
        return result
    
    #Реализация API для продажи медикамента без рецепта
    def add_sale_only_medicament(self,unical_number,worker_number,person):
        validation_result=self._medicament_validate(unical_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._person_validate(person)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.add_sale_only_medicament(unical_number,worker_number,person)
        return result
    
    #Реализация API для продажи медикамента по рецепту
    def add_sale_only_recipe(self,recipe_number,worker_number,person):
        validation_result=self._recipe_validate(recipe_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._person_validate(person)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.add_sale_with_recipe(worker_number,recipe_number,person)
        return result
    
    #Реализация API для отображения продаж по медикаменту
    def display_sale_by_medicament(self,unical_number):
        validation_result=self._medicament_validate(unical_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.display_sale_medicament(unical_number)
        return result
    
    #Реализация API для отображения продаж по рецепту
    def display_sale_by_recipe(self,recipe_number):
        validation_result=self._recipe_validate(recipe_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.display_sale_recipe(recipe_number)
        return result
    
    #Реализация API для отображения продаж по фармацевту
    def display_sale_by_pharmacist(self,worker_number):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.display_sale_worker(worker_number)
        return result
    

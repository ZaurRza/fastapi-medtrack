import Controller.InventoryController as InventoryController
class InventoryAPI(object):
    """Класс для валидации входных данных и реализации API инвентаря"""
    def __init__(self):
        self._controller=InventoryController.InventoryController()
#Валидация данных
    def _unical_number_validate(self,unical_number):
        if unical_number is None:
            return ("ERR",400,"Серийный номер не может быть пустым!")
        
        if unical_number<=0:
            return ("ERR",400,"Серийный номер должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    
#Реализация API
    def display_inventory(self):
        result=self._controller.display_all()
        return result

    def get_inventory_medicament_sorted(self,name,type):
       if name is None or name.strip()=="" or type is None or type.strip()=="":
           return ("ERR",400,"Имя и тип не могут быть пустыми!")
       result=self._controller.get_inventory_medicament_sorted(name,type)
       return result

    def add_to_inventory(self,unical_number):
       validation_result=self._unical_number_validate(unical_number)
       if validation_result[0]=="ERR":
           return validation_result
       result=self._controller.add_medicament_to_inventory(unical_number)
       return result

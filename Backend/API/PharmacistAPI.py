import Controller.PharmacistController as PharmacistController
class PharmacistAPI(object):
    """Класс для валидации входных данных и реализации API фармацевтов"""
    def __init__(self):
        self._controller=PharmacistController.ClassControllerPharmacist()
#Валидация данных
    def _worker_number_validate(self,worker_number):
        if worker_number is None:
            return ("ERR",400,"Номер работника не может быть пустым!")
        
        if worker_number<=0:
            return ("ERR",400,"Номер работника должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")
    
    def _worker_add_validate(self,worker_number,name):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        
        if name is None or name.strip()=="":
            return ("ERR",400,"Имя работника не может быть пустым!")
        
        return ("OK",200,"Валидация прошла успешно!")
    
#Реализация API
    def display_pharmacist(self):
        result=self._controller.display_all()
        return result
    
    def add_pharmacist(self,name,worker_number):
        validation_result=self._worker_add_validate(worker_number,name)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.add_pharmacist(name,worker_number)
        return result
    
    def delete_pharmacist(self,worker_number):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.delete_pharmacist(worker_number)
        return result
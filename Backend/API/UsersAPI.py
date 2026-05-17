import Controller.UsersController as UsersController
class UsersAPI(object):
    """Класс для валидации входных данных и реализации API пользователей"""
    def __init__(self):
        self._controller=UsersController.UsersController()
#Валидация данных
    def _worker_number_validate(self,worker_number):
        if worker_number is None:
            return ("ERR",400,"Номер работника не может быть пустым!")
        
        if worker_number<=0:
            return ("ERR",400,"Номер работника должен быть положительным числом!")
        
        return ("OK",200,"Валидация прошла успешно!")

    def _password_validate(self,password):
        if password is None or password.strip()=="":
            return ("ERR",400,"Пароль не может быть пустым!")
        return ("OK",200,"Валидация прошла успешно!")

    def _add_validate(self,role,worker_number,password):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._password_validate(password)
        if validation_result[0]=="ERR":
            return validation_result
        
        if role is None or role.strip()=="":
            return ("ERR",400,"Роль не может быть пустой!")
        
        if role not in ["admin","pharmacist"]:
            return ("ERR",400,"Роль должна быть 'admin' или 'pharmacist'!")
        
        return ("OK",200,"Валидация прошла успешно!")
#Реализация API
    def display_users(self):
        result=self._controller.display_all()
        return result
    
    def add_user(self,password,worker_number,role):
        validation_result=self._add_validate(role,worker_number,password)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.add_user(password,worker_number,role)
        return result
    
    def delete_user(self,worker_number):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.delete_user(worker_number)
        return result

    def login_user(self,worker_number,password):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        validation_result=self._password_validate(password)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.login_user(worker_number,password)
        return result

    def logout_user(self,worker_number):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.logout_user(worker_number)
        return result

    def check_session(self,worker_number):
        validation_result=self._worker_number_validate(worker_number)
        if validation_result[0]=="ERR":
            return validation_result
        result=self._controller.check_session(worker_number)
        return result
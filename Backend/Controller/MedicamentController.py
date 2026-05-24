from DatabaseConnection import DatabaseConnection
class MedicamentController(object):
    """Класс для реализации логики медикаментов"""
    def __init__(self):
        self._db = DatabaseConnection()

    def _cursor(self):
        mydb=self._db.connect()
        return mydb,mydb.cursor()

    def recipe_check(self, medicament_id):
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM recipe_medicament WHERE medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult = mycursor.fetchone()
        if myresult is not None:
            return True
        return False
#Реализация логики
    #Получение всех медикаментов
    def display_all(self):
        mydb,mycursor = self._cursor()
        sql = "SELECT name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed FROM medicament;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"name":x[0],"price":x[1],"unical_number":x[2],"production_date":x[3],"expiration_date":x[4],"production_country":x[5],"type":x[6],"recipe_needed":x[7]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Добавление медикамента
    def add_medicament(self,name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed):
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is not None:
            return ("ERR",406,"Такой серийный номер уже существует!")
        sql= "INSERT INTO medicament (name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql,(name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed))
        mydb.commit()
        return ("OK",201,"Успешно записано",{"name":name,"price":price,"unical_number":unical_number,"production_date":production_date,"expiration_date":expiration_date,"production_country":production_country,"type":type,"recipe_needed":recipe_needed})
    
    #Удаление медикамента
    def delete_medicament(self,unical_number):
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого серийного номера не существует!")
        medicament_id=myresult[0]
        if self.recipe_check(medicament_id):
            return ("ERR",406,"Невозможно удалить медикамент, так как он используется в рецепте!")
        sql= "DELETE FROM medicament WHERE id=%s"
        mycursor.execute(sql,(medicament_id,))
        mydb.commit()
        return ("OK",200,"Успешно удалено",{"unical_number":unical_number})
    
    #Получение медикамента по серийному номеру
    def display_medicament_exact(self,unical_number):
        mydb,mycursor = self._cursor()
        sql = "SELECT name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого серийного номера не существует!")
        obj={"name":myresult[0],"price":myresult[1],"unical_number":myresult[2],"production_date":myresult[3],"expiration_date":myresult[4],"production_country":myresult[5],"type":myresult[6],"recipe_needed":myresult[7]}
        return ("OK",201,"Успешно найдено",obj)
    
    #Изменение медикамента
    def change_medicament(self,name,price,unical_number,production_date,expiration_date,production_country,type,recipe_needed):
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого серийного номера не существует!")
        sql= "UPDATE medicament SET name=%s,price=%s,production_date=%s,expiration_date=%s,production_country=%s,type=%s,recipe_needed=%s WHERE unical_number=%s"
        mycursor.execute(sql,(name,price,production_date,expiration_date,production_country,type,recipe_needed,unical_number))
        mydb.commit()
        return ("OK",200,"Успешно изменено",{"name":name,"price":price,"unical_number":unical_number,"production_date":production_date,"expiration_date":expiration_date,"production_country":production_country,"type":type,"recipe_needed":recipe_needed})
    

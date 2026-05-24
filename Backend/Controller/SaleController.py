from DatabaseConnection import DatabaseConnection
class SaleController(object):
    """Класс для реализации логики продаж"""
    def __init__(self):
        self._mydb = DatabaseConnection().connect()
#Реализация логики
    #Получение всех продаж
    def display_all(self):
        mycursor = self._mydb.cursor()
        sql = "SELECT medicament.unical_number,pharmacist.worker_number,recipe.recipe_number,sale.sale_date FROM sale LEFT JOIN medicament ON medicament.id = sale.medicament_id JOIN pharmacist ON pharmacist.id = sale.pharmacist_id LEFT JOIN recipe ON recipe.id = sale.recipe_id;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"unical_number":x[0],"worker_number":x[1],"recipe_number":x[2],"sale_date":x[3]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Добавление продажи без рецепта
    def add_sale_only_medicament(self,unical_number,worker_number,person):
        mycursor = self._mydb.cursor()
        sql = "SELECT id,recipe_needed FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого серийного номера не существует!")
        if myresult[1]=='1':
            return ("ERR",406,"Невозможно продать медикамент, так как он требует рецепт!")
        medicament_id=myresult[0]
        sql = "SELECT id FROM inventory WHERE medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого медикамента нет в инвентаре!")
        sql="SELECT id FROM recipe_medicament WHERE medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult=mycursor.fetchone()
        if myresult is not None:
            return ("ERR",406,"Невозможно продать медикамент, так как он используется в рецепте!")
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT id FROM sale WHERE medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult = mycursor.fetchone()
        if myresult is not None:
            return ("ERR",406,"Такая продажа уже существует!")
        sql= "INSERT INTO sale (pharmacist_id,medicament_id,sale_date,person_to) VALUES (%s,%s,NOW(),%s)"
        mycursor.execute(sql,(pharmacist_id,medicament_id,person))
        self._mydb.commit()
        sql="UPDATE medicament SET sold='1' WHERE id=%s"
        mycursor.execute(sql,(medicament_id,))
        self._mydb.commit()
        sql="DELETE FROM inventory WHERE medicament_id=%s"
        mycursor.execute(sql,(medicament_id,))
        self._mydb.commit()
        return ("OK",201,"Успешно записано",{"unical_number":unical_number,"worker_number":worker_number,"person":person})
    
    #Добавление продажи с рецептом
    def add_sale_with_recipe(self,worker_number,recipe_number,person):
        mycursor = self._mydb.cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT id FROM recipe WHERE recipe_number=%s;"
        mycursor.execute(sql,(recipe_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера рецепта не существует!")
        recipe_id=myresult[0]
        sql = "SELECT id FROM sale WHERE recipe_id=%s;"
        mycursor.execute(sql,(recipe_id,))
        myresult = mycursor.fetchone()
        if myresult is not None:
            return ("ERR",406,"Такая продажа уже существует!")
        sql= "INSERT INTO sale (pharmacist_id,recipe_id,sale_date,person_to) VALUES (%s,%s,NOW(),%s)"
        mycursor.execute(sql,(pharmacist_id,recipe_id,person))
        self._mydb.commit()
        sql="SELECT medicament_id FROM recipe_medicament WHERE recipe_id=%s"
        mycursor.execute(sql,(recipe_id,)) 
        myresult = mycursor.fetchall()
        for x in myresult:
            medicament_id=x[0]
            sql="DELETE FROM inventory WHERE medicament_id=%s"
            mycursor.execute(sql,(medicament_id,))
            self._mydb.commit()
            sql="UPDATE medicament SET sold='1' WHERE id=%s"
            mycursor.execute(sql,(medicament_id,))
            self._mydb.commit()
        return ("OK",201,"Успешно записано",{ "worker_number":worker_number,"recipe_number":recipe_number,"person":person })
    
    #Показать продажу по серийному номеру медикамента
    def display_sale_medicament(self,unical_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого серийного номера не существует!")
        medicament_id=myresult[0]
        sql = "SELECT recipe_id FROM recipe_medicament WHERE medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult = mycursor.fetchone()
        #Если медикамент используется в рецепте, то ищем продажу по номеру рецепта
        if myresult is not None:
            recipe_id=myresult[0]
            sql = "SELECT pharmacist.worker_number,recipe.recipe_number,sale.sale_date,sale.person_to FROM sale JOIN pharmacist on pharmacist.id=sale.pharmacist_id LEFT JOIN recipe on recipe.id=sale.recipe_id WHERE sale.recipe_id=%s;"
            mycursor.execute(sql,(recipe_id,))
            myresult = mycursor.fetchall()
            if not myresult:
                return ("ERR",404,"Такой продажи не существует!")
            obj=[]
            for x in myresult:
                obj.append({"worker_number":x[0],"recipe_number":x[1],"sale_date":x[2],"person_to":x[3]})
            return ("OK",201,"Успешно найдено",obj)
        #Если медикамент не используется в рецепте, то ищем продажу по серийному номеру медикамента
        sql = "SELECT pharmacist.worker_number,medicament.name,sale.sale_date,sale.person_to FROM sale JOIN pharmacist on pharmacist.id=sale.pharmacist_id LEFT JOIN medicament on medicament.id=sale.medicament_id WHERE sale.medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult = mycursor.fetchall()
        if not myresult:
            return ("ERR",404,"Такой продажи не существует!")
        obj=[]
        for x in myresult:
            obj.append({"worker_number":x[0],"name":x[1],"sale_date":x[2],"person_to":x[3]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Показать продажу по номеру рецепта
    def display_sale_recipe(self,recipe_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id FROM recipe WHERE recipe_number=%s;"
        mycursor.execute(sql,(recipe_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера рецепта не существует!")
        recipe_id=myresult[0]
        sql = "SELECT id FROM sale WHERE recipe_id=%s;"
        mycursor.execute(sql,(recipe_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такой продажи не существует!")
        sql = "SELECT pharmacist.worker_number,recipe.recipe_number,sale.sale_date,sale.person_to FROM sale JOIN pharmacist on pharmacist.id=sale.pharmacist_id LEFT JOIN recipe on recipe.id=sale.recipe_id WHERE sale.recipe_id=%s;"
        mycursor.execute(sql,(recipe_id,))
        myresult = mycursor.fetchall()
        obj=[]
        sql="SELECT medicament.name FROM medicament LEFT JOIN recipe_medicament on medicament.id=recipe_medicament.medicament_id WHERE recipe_medicament.recipe_id=%s"
        mycursor.execute(sql,(recipe_id,))
        meds=mycursor.fetchall()
        for x in myresult:
            obj.append({"worker_number":x[0],"recipe_number":x[1],"sale_date":x[2],"person_to":x[3],"medicament_list":meds})
        return ("OK",201,"Успешно найдено",obj)
    
    #Показать продажу по номеру работника
    def display_sale_worker(self,worker_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT id FROM sale WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такой продажи не существует!")
        sql = "SELECT recipe.recipe_number,medicament.unical_number,sale.sale_date,sale.person_to FROM sale JOIN pharmacist on pharmacist.id=sale.pharmacist_id LEFT JOIN recipe on recipe.id=sale.recipe_id LEFT JOIN medicament on medicament.id=sale.medicament_id WHERE sale.pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"recipe_number":x[0],"unical_number":x[1],"sale_date":x[2],"person_to":x[3]})
        return ("OK",201,"Успешно найдено",obj)
    

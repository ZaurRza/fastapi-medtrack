from DatabaseConnection import DatabaseConnection
class RecipeController(object):
    """Класс для реализации логики рецептов"""
    def __init__(self):
        self._mydb = DatabaseConnection().connect()
#Реализация логики
    #Получение всех рецептов
    def display_all(self):
        mycursor = self._mydb.cursor()
        sql = "SELECT DISTINCT recipe_number,organization,doctor,patient,recipe_date FROM recipe;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"recipe_number":x[0],"organization":x[1],"doctor":x[2],"patient":x[3],"date":x[4]})
        return ("OK",201,"Успешно найдено",obj)

    #Получение рецепта по номеру
    def display_recipe_exact(self,recipe_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id,recipe_number FROM recipe WHERE recipe_number = %s"
        mycursor.execute(sql,(recipe_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого рецепта не существует!")
        recipe_id=myresult[0]
        sql= "SELECT name,unical_number,organization ,doctor,patient ,recipe_needed FROM(SELECT recipe_id,name,unical_number,recipe_needed FROM recipe_medicament JOIN medicament on medicament_id=medicament.id WHERE recipe_id=%s) rm JOIN recipe on recipe.id=rm.recipe_id;"
        mycursor.execute(sql,(recipe_id,))
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"medicament_name":x[0],"unical_number":x[1],"organization":x[2],"doctor":x[3],"patient":x[4],"is_needed":x[5]})
        return ("OK",201,"Успешно найдено",obj)

    #Добавление рецепта
    def add_recipe(self,recipe_number,organization,doctor,patient,recipe_date,medicament_list):
        mycursor = self._mydb.cursor()
        sql="SELECT id FROM recipe WHERE recipe_number=%s"
        mycursor.execute(sql,(recipe_number,))
        myresult=mycursor.fetchone()
        if myresult is not None:
                return ("ERR",406,"Такой рецепт уже существует!")
        for medicament in medicament_list:
            sql="SELECT id,sold FROM medicament WHERE unical_number=%s"
            mycursor.execute(sql,(medicament,))
            myresult=mycursor.fetchone()
            if myresult is None:
                return ("ERR",404,"Такой медикамент не существует!")
            if myresult[1] == '1':
                return ("ERR",406,"Этот медикамент уже продан!")
            sql="SELECT id FROM recipe_medicament WHERE medicament_id=%s"
            mycursor.execute(sql,myresult)
            myresult=mycursor.fetchone()
            if myresult is not None:
                return ("ERR",406,"Этот медикамент уже в другом рецепте!")
        sql="INSERT INTO recipe (organization,doctor,patient,recipe_number,recipe_date) VALUES (%s,%s,%s,%s,%s)"
        mycursor.execute(sql,(organization,doctor,patient,recipe_number,recipe_date))
        self._mydb.commit()
        recipe_id=mycursor.lastrowid
        medicaments_recipe_id=[]
        for number in medicament_list:
            sql="SELECT id FROM medicament WHERE unical_number=%s"
            mycursor.execute(sql,(number,))
            myresult=mycursor.fetchone()
            medicaments_recipe_id.append((recipe_id,myresult[0]))
        sql="INSERT INTO recipe_medicament (recipe_id,medicament_id) VALUES (%s,%s)"
        mycursor.executemany(sql,medicaments_recipe_id)
        self._mydb.commit()
        return ("OK",200,"Рецепт успешно добавлен!",{"recipe_id": recipe_id})
    
    #Удаление рецепта
    def delete_recipe(self,recipe_number):  
        mycursor = self._mydb.cursor()
        sql="SELECT id FROM recipe WHERE recipe_number=%s"
        mycursor.execute(sql,(recipe_number,))
        myresult=mycursor.fetchone()
        if myresult is None:
                return ("ERR",404,"Такого рецепта не существует!")
        recipe_id=myresult[0]
        sql="DELETE FROM recipe WHERE id=%s"
        mycursor.execute(sql,(recipe_id,))
        self._mydb.commit()
        return ("OK",200,"Рецепт успешно удалён!",{"recipe_id": recipe_id})

from DatabaseConnection import DatabaseConnection
class InventoryController(object):
    """Класс для реализации логики инвентаря"""
    def __init__(self):
        self._mydb = DatabaseConnection().connect()

#Реализация логики
    #Получение всех медикаментов в инвентаре
    def display_all(self):
        mycursor=self._mydb.cursor()
        sql = "SELECT medicament_id,name,price,arrival_date,unical_number FROM inventory JOIN medicament on inventory.medicament_id=medicament.id WHERE medicament.sold=0;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"id":x[0],"name":x[1],"price":x[2],"date_arrival":x[3],"serial_num":x[4]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Добавление медикамента в инвентарь
    def get_inventory_medicament_sorted(self,name,type):
        mycursor = self._mydb.cursor()
        sql = "SELECT medicament.unical_number,medicament.name,medicament.type,medicament.expiration_date FROM inventory JOIN medicament on inventory.medicament_id=medicament.id LEFT JOIN recipe_medicament on recipe_medicament.medicament_id=medicament.id WHERE medicament.name=%s AND medicament.type=%s AND medicament.sold=0 AND recipe_medicament.id IS NULL ORDER BY medicament.expiration_date ASC;"
        mycursor.execute(sql,(name,type))
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"unical_number":x[0],"name":x[1],"type":x[2],"expiration_date":x[3]})
        return ("OK",201,"Успешно найдено",obj)

    def add_medicament_to_inventory(self,unical_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id,sold FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого медикамента не существует!")
        medicament_id=myresult[0]
        sold=myresult[1]
        if sold:
            return ("ERR",406,"Невозможно добавить медикамент в инвентарь, так как он уже продан!")
        sql = "SELECT id FROM inventory WHERE medicament_id=%s;"
        mycursor.execute(sql,(medicament_id,))
        myresult = mycursor.fetchone()
        if myresult is not None:
           return ("ERR",406,"Такой медикамент уже в инвентаре!")
        sql= "INSERT INTO inventory (medicament_id,arrival_date) VALUES (%s,NOW())"
        mycursor.execute(sql,(medicament_id,))
        self._mydb.commit()
        return ("OK",201,"Успешно записано",{"medicament_id":medicament_id})

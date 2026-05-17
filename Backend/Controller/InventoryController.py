from DatabaseConnection import DatabaseConnection
class InventoryController(object):
    """Класс для реализации логики инвентаря"""
    def __init__(self):
        self._mydb = DatabaseConnection().connect()

#Реализация логики
    #Получение всех медикаментов в инвентаре
    def display_all(self):
        mycursor=self._mydb.cursor()
        sql = "SELECT medicament_id,name,price,arrival_date,unical_number FROM inventory JOIN medicament on inventory.medicament_id=medicament.id;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"id":x[0],"name":x[1],"price":x[2],"date_arrival":x[3],"serial_num":x[4]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Добавление медикамента в инвентарь
    def add_medicament_to_inventory(self,unical_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id,sold FROM medicament WHERE unical_number=%s;"
        mycursor.execute(sql,(unical_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,myresult)
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

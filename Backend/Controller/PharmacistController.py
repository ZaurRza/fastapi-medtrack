from DatabaseConnection import DatabaseConnection
class ClassControllerPharmacist(object):
    """Класс для реализации логики фармацевтов"""
    def __init__(self):
        self._mydb = DatabaseConnection().connect()
#Реализация логики
    #Получение всех фармацевтов
    def display_all(self):
        mycursor = self._mydb.cursor()
        sql="SELECT * FROM pharmacist;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"id":x[0],"name":x[1],"worker_number":x[2]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Добавление фармацевта
    def add_pharmacist(self,name,worker_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is not None:
            return ("ERR",406,"Такой номер работника уже существует!")
        sql="INSERT INTO pharmacist (name,worker_number) VALUES (%s,%s)"
        mycursor.execute(sql,(name,worker_number))
        self._mydb.commit()
        return ("OK",201,"Успешно записано",{"name":name,"worker_number":worker_number})
    
    #Удаление фармацевта
    def delete_pharmacist(self,worker_number):
        mycursor = self._mydb.cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        sql="DELETE FROM pharmacist WHERE worker_number=%s"
        mycursor.execute(sql,(worker_number,))
        self._mydb.commit()
        return ("OK",200,"Успешно удалено",{"worker_number":worker_number})

from DatabaseConnection import DatabaseConnection
import bcrypt
class UsersController(object):
    """Класс для реализации логики пользователей"""
    def __init__(self):
        self._db = DatabaseConnection()

    def _cursor(self):
        mydb=self._db.connect()
        return mydb,mydb.cursor()

    def _hash_password(self,password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def _check_password(self,password,hashed):
        if isinstance(hashed, bytes):
            return bcrypt.checkpw(password.encode('utf-8'), hashed)
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    #Автоматическое отключение пользователей, которые были онлайн больше часа
    def _logout_old_sessions(self):
        mydb,mycursor = self._cursor()
        sql = "UPDATE users SET is_online=0 WHERE is_online=1 AND last_log < (NOW() - INTERVAL 1 HOUR)"
        mycursor.execute(sql)
        mydb.commit()
    
#Реализация логики
    #Получение всех пользователей
    def display_all(self):
        self._logout_old_sessions()
        mydb,mycursor = self._cursor()
        sql = "SELECT users.id,pharmacist.name,pharmacist.worker_number,users.role,users.is_online,users.last_log FROM users JOIN pharmacist ON users.pharmacist_id = pharmacist.id;"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        obj=[]
        for x in myresult:
            obj.append({"id":x[0],"name":x[1],"worker_number":x[2],"role":x[3],"is_online":x[4],"last_log":x[5]})
        return ("OK",201,"Успешно найдено",obj)
    
    #Добавление пользователя
    def add_user(self,password,worker_number,role):
        password = self._hash_password(password)
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT id FROM users WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is not None:
            return ("ERR",406,"Такой пользователь уже существует!")
        sql="INSERT INTO users (password,pharmacist_id,role,is_online,last_log) VALUES (%s,%s,%s,0,NOW())"
        mycursor.execute(sql,(password,pharmacist_id,role))
        mydb.commit()
        return ("OK",201,"Успешно записано",{"worker_number":worker_number,"role":role})
    
    #Удаление пользователя
    def delete_user(self,worker_number):
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT id FROM users WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого пользователя не существует!")
        sql="DELETE FROM users WHERE pharmacist_id=%s"
        mycursor.execute(sql,(pharmacist_id,))
        mydb.commit()
        return ("OK",200,"Успешно удалено",{"worker_number":worker_number})
    
    #Логин пользователя
    def login_user(self,worker_number,password):
        self._logout_old_sessions()
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT password,role FROM users WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого пользователя не существует!")
        if not self._check_password(password, myresult[0]):
            return ("ERR",401,"Неверный пароль!")
        sql = "UPDATE users SET is_online=1,last_log=NOW() WHERE pharmacist_id=%s"
        mycursor.execute(sql,(pharmacist_id,))
        mydb.commit()
        return ("OK",200,"Успешный вход!",{"worker_number":worker_number,"role":myresult[1]})

    #Логаут пользователя
    def mobile_login_user(self,worker_number,password):
        self._logout_old_sessions()
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Worker number does not exist!")
        pharmacist_id=myresult[0]
        sql = "SELECT password,role FROM users WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"User does not exist!")
        if not self._check_password(password, myresult[0]):
            return ("ERR",401,"Wrong password!")
        return ("OK",200,"Successful mobile login!",{"worker_number":worker_number,"role":myresult[1]})

    def logout_user(self,worker_number):
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT id FROM users WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого пользователя не существует!")
        sql = "UPDATE users SET is_online=0 WHERE pharmacist_id=%s"
        mycursor.execute(sql,(pharmacist_id,))
        mydb.commit()
        return ("OK",200,"Пользователь вышел из аккаунта!",{"worker_number":worker_number})
    
    def check_session(self,worker_number):
        self._logout_old_sessions()
        mydb,mycursor = self._cursor()
        sql = "SELECT id FROM pharmacist WHERE worker_number=%s;"
        mycursor.execute(sql,(worker_number,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого номера работника не существует!")
        pharmacist_id=myresult[0]
        sql = "SELECT is_online FROM users WHERE pharmacist_id=%s;"
        mycursor.execute(sql,(pharmacist_id,))
        myresult = mycursor.fetchone()
        if myresult is None:
            return ("ERR",404,"Такого пользователя не существует!")
        if myresult[0]==1:
            return ("OK",200,"Сессия активна!",{"online":True,"worker_number":worker_number})
        else:
            return ("OK",200,"Сессия неактивна!",{"online":False,"worker_number":worker_number})

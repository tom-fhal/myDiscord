import mysql.connector
import datetime

class Query:
    def __init__(self):
        self.conn = mysql.connector.connect(
                                        host='localhost',
                                        database='discord',
                                        user='root',
                                        password='')
    
    def getServ(self,user_id) -> list:
        cursor = self.conn.cursor()
        sqlQuery= f"SELECT nom_serveur,serveur.id_serveur FROM serveur INNER JOIN membres ON serveur.id_serveur = membres.id_serveur WHERE membres.id_utilisateur LIKE {int(user_id)};"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getUserId(self,email) -> int:
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT id_utilisateur FROM utilisateurs WHERE email_utilisateur LIKE '{email}';"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()[0][0]
        cursor.close()
        return int(result)


    def getChannelServ(self,serv_id) -> list:
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT nom_canal,port FROM canaux WHERE id_serveur LIKE {serv_id};"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getChannelId(self,nom_channel) -> int:
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT id_canal FROM canaux WHERE nom_canal LIKE '{nom_channel}';"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        return int(result[0][0])
    
    def getUsername(self,email):
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT nom_utilisateur FROM utilisateurs WHERE email_utilisateur LIKE '{email}';"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        return result[0][0]
    
    def isAdmin(self,id_user,id_server) -> bool:
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT id_utilisateur,id_serveur FROM serveur WHERE id_serveur LIKE {id_server} AND id_utilisateur LIKE {id_user};"
        cursor.execute(sqlQuery)
        if len(cursor.fetchall()) > 0:
            cursor.close()
            return True
        cursor.close()
        return False
    
    def getNoMember(self,id_server) -> list:
        def user() :
            cursor = self.conn.cursor()
            sqlQuery = f"SELECT nom_utilisateur FROM utilisateurs;"
            cursor.execute(sqlQuery)
            result = []
            for users in cursor.fetchall():
                result.append(users[0])
            cursor.close()
            return result
        users = user()
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT nom_utilisateur FROM utilisateurs INNER JOIN membres on membres.id_utilisateur = utilisateurs.id_utilisateur WHERE id_serveur LIKE {id_server};"
        cursor.execute(sqlQuery)
        for userIn in cursor.fetchall():
            users.remove(userIn[0])
        return users

    def getUserIdWithName(self,username) -> int:
        cursor = self.conn.cursor()
        sqlQuery = f"SELECT id_utilisateur FROM utilisateurs WHERE nom_utilisateur LIKE '{username}';"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()[0][0]
        cursor.close()
        return int(result)
    
    def getAllChannels(self) -> list:
        cursor = self.conn.cursor()
        sqlQuery = "SELECT * FROM canaux;"
        cursor.execute(sqlQuery)
        return cursor.fetchall()
       
    def addUserInServ(self,serv_id,users): 
        cursor = self.conn.cursor()
        id = self.getUserIdWithName(users)
        format = "%Y-%m-%d"
        today = datetime.datetime.today().strftime(format)
        sqlQuery = f"INSERT INTO membres (id_utilisateur,id_serveur,date_joined) VALUES ('{id}','{serv_id}','{today}');"
        cursor.execute(sqlQuery)
        self.conn.commit()
        cursor.close()

    def AddNewMessage(self,id_canal,text,name):
        cursor = self.conn.cursor()
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        now = datetime.datetime.now()
        heure = now.strftime("%H:%M:%S")
        sqlQuery = f'INSERT INTO messages (text,date_envoi,heure_envoi,id_utilisateur,id_canal) VALUES ("{text}","{today}","{heure}",{self.getUserIdWithName(name)},{id_canal});'
        cursor.execute(sqlQuery)
        self.conn.commit()
        cursor.close()
    
    def setNewUser(self,email,username,password):
        cursor = self.conn.cursor()
        sqlQuery = f"INSERT INTO utilisateurs (nom_utilisateur,email_utilisateur,mot_de_passe) VALUES ('{username}','{email}','{password}');"
        cursor.execute(sqlQuery)
        self.conn.commit()
        cursor.close()

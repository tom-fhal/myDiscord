from tkinter import *
from tkinter import ttk
from customtkinter import *
from connect_bd import Query
from CTkMessagebox import CTkMessagebox
from client import * 
import time
import threading

set_appearance_mode("blue")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")

window = CTk()
window.geometry(f"{1100}x{580}")
window.title("Discord")
window.resizable(True, True)
query = Query()


def deleteAll():
    for widgets in window.winfo_children():
        widgets.grid_forget()
        widgets.place_forget()

def inscription():
    deleteAll()

    def confirm():
        if mdp.get() != confirmMdp.get():
            CTkMessagebox(title="erreur",message="Les mots de passe sont différents.",icon="cancel")
        elif "@" not in email.get() and "." not in email.get():
            CTkMessagebox(title="erreur",message="L'email est incorrecte.",icon="cancel")
        else : 
            query.setNewUser(email.get(),pseudo.get(),confirmMdp.get())
            mb = CTkMessagebox(message="Vous êtes maintenant inscris sur Discord !",icon="check", option_1="LETSGO !")
            if mb.get() == "LETSGO !" : 
                deleteAll()
                connexion()


    CTkLabel(window,text="Inscription",font=("Roboto",35)).grid(row=0,column=0)

    form_inscri = CTkFrame(window)
    form_inscri.grid(row=1,column=0)

    CTkLabel(form_inscri,text="E-mail :",font=("Roboto",20)).grid(row=0,column=0)
    CTkLabel(form_inscri,text="Pseudo :",font=("Roboto",20)).grid(row=1,column=0)
    CTkLabel(form_inscri,text="Mot de passe : ",font=("Roboto",20)).grid(row=2,column=0)
    CTkLabel(form_inscri,text="Confirmez le mot de passe :",font=("Roboto",20)).grid(row=3,column=0)

    email = CTkEntry(form_inscri,placeholder_text="Adresse E-Mail")
    pseudo = CTkEntry(form_inscri,placeholder_text="Pseudo")
    mdp = CTkEntry(form_inscri,placeholder_text="Mot de Passe",show="*")
    confirmMdp = CTkEntry(form_inscri,placeholder_text="Confirmer mot de passe",show="*")
    
    email.grid(row=0,column=1,pady=10)
    pseudo.grid(row=1,column=1,pady=10)
    mdp.grid(row=2,column=1,pady=10)
    confirmMdp.grid(row=3,column=1,pady=10)

    CTkButton(window,text="Inscription",command=confirm).grid(row=2,column=0,pady=10)
    
def menu(email):
    deleteAll()
    #Liste des connexions vers chacun des ports de canal discord
    listConn = []

    def displayMessage(client_socket):        

        def sendMessage():
            client_socket.send_message(send_entry.get())
            send_entry.delete(0,END)

        client_socket.tabview.grid(row=0,column=0,sticky="n")

        frame_send = CTkFrame(frame_chat)
        frame_send.grid(row=1,column=0,sticky="s")


        send_entry = CTkEntry(frame_send,placeholder_text="Envoyez un message...",width=500)
        send_button = CTkButton(frame_send ,fg_color="transparent", text="Envoyer",border_width=2, text_color=("gray10", "#DCE4EE"),command= sendMessage)
        send_entry.grid(column=0,row=1,padx=10)
        send_button.grid(column=1,row=1)

        

    def addUser(serv_id):
        #Nouvelle fenêtre pour ajouter des utilisateurs
        screen = CTkToplevel()

        def add(serv_id,user):
            query.addUserInServ(serv_id,user)
            CTkMessagebox(message="Utilisateur ajouté avec succès",icon="check", option_1="Ok")
        
        i = 0
        for users in query.getNoMember(serv_id):
            CTkLabel(screen,text=f"{users} : ").grid(row=i,column=0)
            CTkButton(screen,text="Ajouter l'utilisateur",command=lambda : add(serv_id,users)).grid(row=i,column=1)
            i+=1

    def displayChannels(serv_id):
        #Affiche la liste des canaux dispo dans un serveur
        listChannel = query.getChannelServ(serv_id)
        i = 0
        for channel in listChannel:
            listConn.append(ChatRoomClient("localhost",channel[1],query.getUsername(email),frame_chat,query.getChannelId(str(channel[0]))))
            threading.Thread(target=listConn[i].connect).start()
            CTkButton(frame_channel,text=channel[0],width=165,height=15,bg_color="#2b2d31",command=lambda i=i: displayMessage(listConn[i]) ).grid(row = i,column = 1,sticky="n",pady=10)
            i+=1
        if query.isAdmin(query.getUserId(email),serv_id):
             CTkButton(frame_channel,text="Ajouter un utilisateur",width=165,height=15,bg_color="#2b2d31",fg_color="#249A07",command= lambda : addUser(serv_id)).grid(row = i+1,column = 1,sticky="s",pady=30)


    frame_serv = CTkFrame(window,fg_color="#1e1f22",bg_color="#1e1f22",width=140,height=1000)
    frame_serv.grid(row=0,column=0,sticky="nw")

    frame_channel = CTkFrame(window,fg_color="#2b2d31",bg_color="#2b2d31",width=180,height=1000)
    frame_channel.grid(row=0,column=1,sticky="n")

    frame_chat = CTkFrame(window,fg_color="#313338",width=800,height=1000)
    frame_chat.grid(row=0,column=2,sticky="ne")

    list_serv = query.getServ(query.getUserId(email))
    i = 0
    for serveur in list_serv:
        CTkButton(frame_serv,text=serveur[0],width=50,bg_color="#1e1f22",command= lambda : displayChannels(int(serveur[1])) ).grid(row = i,column = 0,sticky="n",pady=10,padx=20)
        i+=1

    # CTkButton(frame_serv,text="Créez un serveur",width=50).grid(row = i,column=0,sticky="s")



def connexion():
    def verifPasswd(email,passwd):
        cursor = query.conn.cursor()
        sqlQuery = "SELECT email_utilisateur,mot_de_passe FROM utilisateurs;"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()

        userInDb = False
        for data in result : 
            userInDb
            if data[0] == email and data[1] == passwd:
                userInDb = True 
                menu(email)
                cursor.close()
                return 0
        CTkMessagebox(title="Erreur", message="E-mail ou mot de passe incorrect", icon="cancel")
        cursor.close()

    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    
    CTkLabel(window,text="Discord",font=("Roboto",50),text_color="purple").grid(row=0,column=0)

    conn_form = CTkFrame(window)
    conn_form.grid(row=1,column=0)
    

    CTkLabel(conn_form,text="E-mail : ",font=("Roboto",20)).grid(row=0,column=0)
    CTkLabel(conn_form,text="Mot de passe : ",font=("Roboto",20)).grid(row=1,column=0)


    email = CTkEntry(conn_form,placeholder_text="Adresse e-mail")
    password = CTkEntry(conn_form,placeholder_text="Mot de passe",show="*")
    connectButton = CTkButton(conn_form,text="Connexion",command= lambda : verifPasswd(email.get(),password.get())) 
    email.grid(row=0,column=1)
    password.grid(row=1,column=1)
    connectButton.grid(row=2,column=1)
    
    CTkLabel(conn_form,text="Pas de compte ? ",font=("Roboto",10)).grid(row=3,column=0)
    inscriButton = CTkButton(conn_form,text="Inscrivez vous",command=inscription)
    inscriButton.grid(row=3,column=1,pady=10)


connexion()


window.mainloop()
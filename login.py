from PyQt5 import uic, QtWidgets, QtCore, QtGui
from datetime import datetime
from email.message import EmailMessage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import face_recognition
import os
import re
import sys
import smtplib
import random
import threading
import time
import sqlite3
import Data_Base_Config 

# database name = users // table name = users e logs
# MODULES
    # pip install PyQt5
    # pip install mysql-connector
    # pip install opencv-python
    # pip install face_recognition
    # pip install db-sqlite3

#conecção com o DataBase
data = sqlite3.connect('DataBase.db')

# botoes de pagina para pagina
def exit():
    home.close()
def abre_login():
    home.close()
    root.close()
    login.show()
def abre_home():
    login.close()
    home.show()
def abre_new_user():
    root.close()
    new_user.show()
def voltar_new_user():
    new_user.close()
    root.show()
def voltar_all_users():
    all_users.close()
    root.show()
def voltar_home():
    unlock.close()
    home.show()
def voltar_login():
    user_area.close()
    login.show()
def voltar_root():
    all_logs.close()
    root.show()
def voltar_root_2():
    root.show()
    user_some_logs.close()
def pag_2_way_to_home():
    pag_2_way.close()
    home.show()
def pin_to_home():
    home.show()
    pin.close()

# users dada (passwords, login, perfil, logs, etc) BIG STUFF
def submeter_new_user():

    #mensaguens de erro 
    new_user.label_4.setText("")
    new_user.label_8.setText("")
    new_user.label_13.setText("")
    new_user.label_14.setText("")
    new_user.label_15.setText("")
    new_user.label_16.setText("")
    new_user.label_19.setText("")

    # Espaços a preencer (atrbuir nomes/variaveis aos espaços a preencher pelo user)
    nome = new_user.lineEdit.text().upper()
    tlm = new_user.lineEdit_2.text()
    pin = new_user.lineEdit_4.text()
    ano = new_user.lineEdit_7.text()
    dia = new_user.lineEdit_5.text()
    mes = new_user.lineEdit_8.text()
    email = new_user.lineEdit_3.text()

    # Triagem dos dados

    if nome != "" :
        try:
            comando_SQL_Nome = ("SELECT Nome FROM users WHERE Nome = '{}';").format(nome)
            cursor = data.cursor()
            cursor.execute(comando_SQL_Nome)
            cursor = cursor.fetchall()
            nome_database = (cursor[0][0])

            print("nome_database = ", nome_database)

            if nome_database == nome:
                new_user.label_15.setText("O nome já existe")
                nome = 0
        except:
            nome = nome
    elif nome == "" :
        new_user.label_15.setText("Obrigatorio preencher")
        nome = 0

    if tlm != "":
        try:
            tlm = int(tlm)       
        except ValueError:
            tlm = 0
            new_user.label_4.setText("Invalido")
            new_user.lineEdit_2.setText("")
        else:
            if 910000000 < tlm < 969999999:
                tlm = tlm
            else:
                tlm = 0
                new_user.label_4.setText("Numero invalido")
                new_user.lineEdit_2.setText("")
    else:
        tlm = 0
        new_user.label_4.setText("Obrigatorio preencher")
        new_user.lineEdit_2.setText("")

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if email != "":
        if (re.search(regex,email)):
            email = email
        else:
            email = 0
            new_user.label_16.setText("Email invalido")
    else:
        email = 0
        new_user.label_16.setText("Obrigatorio preencher")

    if pin != "":
        try:
            pin = int(pin)
        except ValueError:
            pin = 0
            new_user.label_8.setText("Invalido")
            new_user.lineEdit_4.setText("")
        else:
            if 1000 < pin < 999999:
                pin = pin
            else:
                pin = 0
                new_user.label_8.setText("Pin invalido")
                new_user.lineEdit_4.setText("")
    else:
        pin = 0
        new_user.label_8.setText("Obrigatorio preencher")
        new_user.lineEdit_4.setText("")

    if ano == "" or dia == "" or mes == "":
            new_user.label_13.setText("Obrigatorio preencher")
            data_nascimento = 0       
    else:
        date = datetime.now()
        try:
            ano = int(ano)
        except ValueError:
            ano = 0
            new_user.label_13.setText("Data invalida")
            new_user.lineEdit_7.setText("")
        else:
            if (int(date.strftime("%Y")) - 100) <= ano <= int(date.strftime("%Y")):
                ano = ano
            else :
                ano = 0
                new_user.label_13.setText("Data invalida")
                new_user.lineEdit_7.setText("")

    try:
        mes = int(mes)
    except ValueError:
        mes = 0
        new_user.label_13.setText("Data invalida")
        new_user.lineEdit_8.setText("")
    else :
        if 1 <= mes <= 12 :
            mes = mes 
        else :
            mes = 0
            new_user.label_13.setText("Data invalida")
            new_user.lineEdit_8.setText("")    

    try:
        dia = int(dia)
    except ValueError:
        dia = 0
        new_user.label_13.setText("Data invalida")
        new_user.lineEdit_5.setText("")
    else:
        if mes == 2:
            if 1 <= dia <= 29:
                dia = dia
            else:
                dia = 0 
                new_user.label_13.setText("Data invalida")
                new_user.lineEdit_5.setText("")
        else:
            if 1 <= dia <= 31:
                dia = dia
            else:
                dia = 0 
                new_user.label_13.setText("Data invalida")
                new_user.lineEdit_5.setText("")

    if dia != 0 and mes != 0 and ano != 0:
        data_nascimento = "{}-{}-{}".format(ano, mes, dia)
    else:
        data_nascimento = 0            

    if new_user.radioButton.isChecked():
        genero = "M"
    elif new_user.radioButton_2.isChecked():
        genero = "F"
    elif new_user.radioButton_4.isChecked():
        genero = "Outro"
    else:
        genero = 0  
        new_user.label_14.setText("Obrigatorio preencher")

    print("")
    print("nome: ",nome)
    print("tlm: ",tlm)
    print("email: ",email)
    print("pin: ",pin)
    print("data: ", data_nascimento)
    print("genero: ",genero)
    print("")

    if tlm != 0 and pin != 0 and data_nascimento != 0 and genero != 0 and nome != 0 and email != 0:
        cursor = data.cursor()
        comando_SQL = "INSERT INTO users (nome,tlm,email,pin,data_nascimento,genero) VALUES (?,?,?,?,?,?)"
        dados = (str(nome), str(tlm), str(email),str(pin), str(data_nascimento), genero)
        cursor.execute(comando_SQL, dados)
        data.commit()

        #tirar a foto para o reconhecimento facial
        def tirar_fotos_FACE_ID():
            face_cascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

            cap = cv2.VideoCapture(0)  # seleciona a camera, neste momento esta a default

            i = 0

            while True:

                ret, frame = cap.read()  # ler frame por frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # para conseguir o reconhecimento a frame tem de estar em gray (seguindo a documentação)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) # defenir a escala da frame

                for (x, y, w, h) in faces:
                    #print(x, y, w, h)

                    roi_gray = gray[y:y+h, x:x+w]  # (y=y+altura x=x+cumprimento)
                    roi_color = frame[y:y+h, x:x+w]

                    # CORES:
                    img_nome_cores = "Data_Base_fotos/{}.png".format(nome)
                    cv2.imwrite(img_nome_cores, roi_color)

                    i = i + 1

                if i == 5:
                    break

            cap.release()
            cv2.destroyAllWindows()
        process_Foto = threading.Thread(target= tirar_fotos_FACE_ID)
        process_Foto.start()

        def email_user(subject, body, to):
            msg = EmailMessage()
            msg.set_content(body)
            msg['subject'] = subject
            msg['to'] = to
            # pass do email Seguranca1234
            user = "sistema.seguranca.codigo@gmail.com"
            msg['from'] = user
            password = "sqjvcjmzaxhbzyjt"

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            server.quit()

        texto = str("""        A sua conta foi registada na nossa plataforma com sucesso.
        Os dados referentes à sua conta são:
        
        Nome de utilizador: {}
        Telemóvel: {}
        Género: {}

        Caso haja necessidade de alterar algum dos dados pode fazê-lo posteriormente na Área de Utilizador.
        Obrigado.""".format(str(nome), int(tlm), str(genero)))

        email_user("Conta criada com sucesso.", texto, email)

        new_user.label_19.setText("Novo user criado com sucesso")

        # deixar espaços em branco
        new_user.lineEdit.setText("")
        new_user.lineEdit_2.setText("")
        new_user.lineEdit_3.setText("")
        new_user.lineEdit_4.setText("")
        new_user.lineEdit_5.setText("")
        new_user.lineEdit_8.setText("")
        new_user.lineEdit_7.setText("")
def entrar_login():
    #   melhorar este codigo
def apagar_user():
    if all_users.lineEdit.text() == "":
        pass
    else:
        all_users.label_6.setText("")
        cursor = data.cursor()
        comando_SQL = ("DELETE FROM `users` WHERE `users`. `id` = {}").format(all_users.lineEdit.text())
        cursor.execute(comando_SQL)
        data.commit()
        all_users.lineEdit.setText("")

        all_users.label_6.setText("User apagado com sucesso")
def todos_users():
    root.close()
    all_users.show()

    cursor = data.cursor()
    comando_SQL = " SELECT * FROM users"
    cursor.execute(comando_SQL)
    users_lidos = cursor.fetchall()
    all_users.tableWidget.setRowCount(len(users_lidos))
    all_users.tableWidget.setColumnCount(7)

    for i in range(0, len(users_lidos)):
        for j in range(0, 7):
            all_users.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(users_lidos[i][j])))
def todos_logs():
    root.close()
    all_logs.show()

    cursor = data.cursor()
    comando_SQL = " SELECT * FROM logs"
    cursor.execute(comando_SQL)
    logs_lidos = cursor.fetchall()
    all_logs.tableWidget.setRowCount(len(logs_lidos))
    all_logs.tableWidget.setColumnCount(5)

    for i in range(0, len(logs_lidos)):
        for j in range(0, 5):
            all_logs.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(logs_lidos[i][j])))
def some_logs():
    user_some_logs.show()
    root.close()

    cursor = data.cursor()
    comando_SQL = " SELECT id, Nome FROM users"
    cursor.execute(comando_SQL)
    some_logs = cursor.fetchall()
    user_some_logs.tableWidget.setRowCount(len(some_logs))
    user_some_logs.tableWidget.setColumnCount(2)

    for i in range(0, len(some_logs)):
        for j in range(0, 2):
            user_some_logs.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(some_logs[i][j])))

    def submeter_some_logs():

        id = user_some_logs.lineEdit.text()

        cursor = data.cursor()
        comando_SQL_ID = " SELECT * FROM logs WHERE id = '{}'".format(id)
        cursor.execute(comando_SQL_ID)
        some = cursor.fetchall()

        user_some_logs.tableWidget_2.setRowCount(len(some))
        user_some_logs.tableWidget_2.setColumnCount(5)

        for a in range(0, len(some)):
            for b in range(0, 5):
                user_some_logs.tableWidget_2.setItem(a, b, QtWidgets.QTableWidgetItem(str(some[a][b])))

        user_some_logs.lineEdit.setText("")

    user_some_logs.pushButton_51.clicked.connect(submeter_some_logs)
def abre_unlock():

    home.close()
    unlock.show()

    class Executar:
        def __init__(self):
            self.resposta = "True"
        def exe_Face_ID(self):

            path = "Data_Base_fotos" #local onde as imagens dos users estao guardadas
            imagens = [] # lista de imagens
            nomes = [] #lista de nomes

            lista_nome = os.listdir(path)

            for cl in lista_nome:
                img_na_pasta = cv2.imread(f'{path}/{cl}') #ler as imagens no path
                imagens.append(img_na_pasta) #inserir as imagens na lista imagens
                nomes.append(os.path.splitext(cl)[0]) #inserir os nomes das imagens na lista nomes

            def findEncondings(imagens):
                encode_list = []
                for img in imagens:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #passar as imagens de RGB para BGR
                    encode = face_recognition.face_encodings(img)[0]
                    encode_list.append(encode)
                return encode_list

            encodelistKnown = findEncondings(imagens)

            cap = cv2.VideoCapture(0) #usar camera

            while True:

                if self.resposta == "Stop":
                    break
                else:
                    pass

                success, imagem = cap.read() #ler o que esta a aparecer na camera
                imagem_pequena = cv2.resize(imagem,(0,0),None,0.25,0.25) #fazer o resize da imagem (mete-la mais pequena)
                imagem_pequena = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB) #passar as imagens de RGB para BGR

                face_frame = face_recognition.face_locations(imagem_pequena) #encontar a localização das caras na imagem
                encode_frame = face_recognition.face_encodings(imagem_pequena, face_frame)

                #var so para caso a cara n seja reconhecida, caso seja, vao ser alteradas a seguir
                nome_ecra = "nulo"
                Nome = "zero"

                for encodeframe, faceloc in zip(encode_frame, face_frame):
                    matches = face_recognition.compare_faces(encodelistKnown, encodeframe)
                    face_dis = face_recognition.face_distance(encodelistKnown, encodeframe)
                    #print(face_dis)

                    matcheIndex = np.argmin(face_dis) #fazer o match entre o valores do face_dis com os nomes

                    if matches[matcheIndex]: #fazer o reconhecimento
                        nome_ecra = nomes[matcheIndex]
                        print(nome_ecra)

                        #fazer aparecer retangulos na cara das pessoas
                        #y1,x2,y2,x1 = faceloc
                        #cv2.rectangle(imagem,(x1,y1),(x2,y2),(0,255,0),2) #caixa a volta da cara 
                        #cv2.putText(imagem, nome_ecra, (x1+6,y2+26), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255), 2) #nome da pessoa

                        #fazer input no database 
                        comando_SQL_id = ("SELECT * FROM users WHERE Nome = '{}';").format(nome_ecra)
                        cursor = data.cursor()
                        cursor.execute(comando_SQL_id)
                        cursor = cursor.fetchall()
                        Nome = cursor[0][1]

                    else:
                        pass
                        #nome_ecra = "UNKNOWN"
                        #y1,x2,y2,x1 = faceloc
                        #cv2.rectangle(imagem,(x1,y1),(x2,y2),(0,0,255),2) #caixa a volta da cara 
                        #cv2.putText(imagem, nome_ecra, (x1+6,y2+26), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2) #nome da pessoa

                if nome_ecra == Nome :

                    id = cursor[0][0]
                    Nome_final = cursor[0][1]
                    Local = "Face_ID"
                    Data_Hora = datetime.now()

                    comando_SQL = "INSERT INTO logs (id,Nome,Local,Data,Hora) VALUES (?,?,?,?,?)"
                    dados = (int(id), str(Nome_final), str(Local), Data_Hora, Data_Hora)
                    cursor = data.cursor()
                    cursor.execute(comando_SQL, dados)
                    data.commit()

                    #import connector
                    
                else:
                    pass
        def exe_PIN(self):
            self.resposta = "Stop"

            unlock.close()
            pin.show()

            pin.lineEdit.setText("")
            pin.lineEdit_2.setText("")

            # funções dos botoes
            def do_1():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "1")
            def do_2():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "2")
            def do_3():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "3")
            def do_4():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "4")
            def do_5():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "5")
            def do_6():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "6")
            def do_7():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "7")
            def do_8():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "8")
            def do_9():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "9")
            def do_0():
                pin.lineEdit_2.setText(pin.lineEdit_2.text() + "0")
            def do_clear():
                pin.lineEdit_2.setText(pin.lineEdit_2.text()[0:-1])
            def submeter_pin():

                pin.label_15.setText("")
                pin.label_16.setText("")
                pin.label_17.setText("")

                if pin.lineEdit.text() == "":
                    pin.label_15.setText("Obrigatorio preencher")
                    user_input = 0
                else :
                    user_input = pin.lineEdit.text()

                if pin.lineEdit_2.text() == "":
                    pin.label_16.setText("Obrigatorio preencher")
                    pin_input = 0
                else:
                    pin_input = int(pin.lineEdit_2.text())

                if pin.radioButton.isChecked():
                    enviar = "Email"
                elif pin.radioButton_2.isChecked():
                    enviar = "SMS"
                else:
                    enviar = 0
                    pin.label_17.setText("Obrigatorio preencher")

                print(pin_input, user_input)
                if (user_input != 0) and (pin_input != 0):
                    if user_input == "root" and pin_input == 123456:

                        id = 1
                        Nome = "root"
                        Local = "PIN"
                        Data_Hora = datetime.now()
                        comando_SQL = "INSERT INTO logs (id,Nome,Local,Data,Hora) VALUES (?,?,?,?,?)"
                        dados = (int(id), str(Nome), str(Local), Data_Hora, Data_Hora)
                        cursor = data.cursor()
                        cursor.execute(comando_SQL, dados)
                        data.commit()

                        #print("Porta aberta")

                    elif user_input != "root" :

                        comando_SQL_PIN = ("SELECT * FROM users WHERE Nome = '{}'").format(user_input)
                        cursor = data.cursor(buffered=True)
                        cursor.execute(comando_SQL_PIN)
                        cursor = cursor.fetchall()
                        try:
                            user_database = cursor[0][1]
                            pin_database = int(cursor[0][2])
                            email = (cursor[0][5])

                            if user_database == "":
                                pin.label_15.setText("Obrigatorio preencher")
                            else:
                                if pin_database == pin_input and enviar != 0:
                                    if enviar == "Email":

                                        #formatar-criar-enviar o email
                                        def email_code(subject, body, to):
                                            msg = EmailMessage()
                                            msg.set_content(body)
                                            msg['subject'] = subject
                                            msg['to'] = to
                                            # pass do email: Seguranca1234
                                            user = "sistema.seguranca.codigo@gmail.com"
                                            msg['from'] = user
                                            password = "sqjvcjmzaxhbzyjt"

                                            server = smtplib.SMTP("smtp.gmail.com", 587)
                                            server.starttls()
                                            server.login(user, password)
                                            server.send_message(msg)
                                            server.quit()

                                        #gerar uma chave temporaria e enviar (executar o def email_code)
                                        codigo = int(random.randint(1000, 9999))
                                        chave = str("""O código de autenticação é {}. Este código é apenas válido para uma utilização. Obrigado.""".format(str(codigo)))
                                        email_code("Chave de segurança", chave, email)

                                        pag_2_way.show()
                                        pin.close()

                                        #pagina de confirmação de 2 fatores
                                        def submeter_2_way():
                                            
                                            user_input_codigo = int(pag_2_way.lineEdit_3.text())
                                            
                                            if codigo == user_input_codigo:

                                                comando_SQL_logs = ("SELECT * FROM users WHERE Nome = '{}'").format(user_input)
                                                cursor = data.cursor(buffered=True)
                                                cursor.execute(comando_SQL_logs)
                                                cursor = cursor.fetchall()

                                                id = cursor[0][0]
                                                Nome = cursor[0][1]
                                                Local = "PIN"
                                                Data_Hora = datetime.now()

                                                comando_SQL = "INSERT INTO logs (id,Nome,Local,Data,Hora) VALUES (?,?,?,?,?)"
                                                dados = (int(id), str(Nome), str(Local), Data_Hora, Data_Hora)
                                                cursor = data.cursor()
                                                cursor.execute(comando_SQL, dados)
                                                data.commit()

                                                pag_2_way.lineEdit_3.setText("")

                                                print("porta aberta com sucesso")

                                                #import connector

                                                pag_2_way.close()
                                                unlock.show()
                                            else:
                                                pag_2_way.label_15.setText("Codigo errado")

                                        pag_2_way.pushButton_16.clicked.connect(submeter_2_way)

                                    else:
                                        pin.label_17.setText("Operação ainda não disponivel")

                                    def do_1():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "1")
                                    def do_2():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "2")
                                    def do_3():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "3")
                                    def do_4():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "4")
                                    def do_5():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "5")
                                    def do_6():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "6")
                                    def do_7():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "7")
                                    def do_8():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "8")
                                    def do_9():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "9")
                                    def do_0():
                                        pag_2_way.lineEdit_3.setText(pag_2_way.lineEdit_3.text() + "0")
                                    def do_clear():
                                        pag_2_way.lineEdit_3.setText("")

                                    # botoes 2_way
                                    pag_2_way.pushButton_14.clicked.connect(do_1)
                                    pag_2_way.pushButton_13.clicked.connect(do_2)
                                    pag_2_way.pushButton_12.clicked.connect(do_3)
                                    pag_2_way.pushButton_11.clicked.connect(do_4)
                                    pag_2_way.pushButton_9.clicked.connect(do_5)
                                    pag_2_way.pushButton_10.clicked.connect(do_6)
                                    pag_2_way.pushButton_8.clicked.connect(do_7)
                                    pag_2_way.pushButton_7.clicked.connect(do_8)
                                    pag_2_way.pushButton_6.clicked.connect(do_9)
                                    pag_2_way.pushButton_15.clicked.connect(do_0)
                                    pag_2_way.pushButton_17.clicked.connect(do_clear)

                                else:
                                    if enviar == 0:
                                        pin.label_17.setText("Obrigatorio preencher")
                                    else:
                                        pin.label_16.setText("PIN incorreto")
                        except:
                            pin.label_15.setText("User não valido")

                    elif user_input == root and pin_input != "123456":
                        pin.label_16.setText("PIN incorreto")
                    else:
                        pass
                else:
                    pass

            # botoes dos numeros etc
            pin.pushButton_14.clicked.connect(do_1)
            pin.pushButton_13.clicked.connect(do_2)
            pin.pushButton_12.clicked.connect(do_3)
            pin.pushButton_11.clicked.connect(do_4)
            pin.pushButton_9.clicked.connect(do_5)
            pin.pushButton_10.clicked.connect(do_6)
            pin.pushButton_8.clicked.connect(do_7)
            pin.pushButton_7.clicked.connect(do_8)
            pin.pushButton_6.clicked.connect(do_9)
            pin.pushButton_15.clicked.connect(do_0)
            pin.pushButton_17.clicked.connect(do_clear)
            pin.pushButton_16.clicked.connect(submeter_pin)
        def voltar_home_3(self):
            self.resposta = "Stop"
            unlock.close()
            home.show()

    Exe = Executar()

    #executar o "exe_face_id" num core diferente, em simultaneo do resto
    process_Face_ID = threading.Thread(target= Exe.exe_Face_ID)
    process_Face_ID.start()

    unlock.pushButton_2.clicked.connect(Exe.exe_PIN)
    unlock.pushButton_3.clicked.connect(Exe.voltar_home_3) 

# janelas
app = QtWidgets.QApplication([])
login = uic.loadUi("Janelas/login_pass.ui")
root = uic.loadUi("Janelas/root.ui")
home = uic.loadUi("Janelas/home.ui")
new_user = uic.loadUi("Janelas/new_user.ui")
all_users = uic.loadUi("Janelas/all_users.ui")
unlock = uic.loadUi("Janelas/unlock.ui")
user_area = uic.loadUi("Janelas/user_area.ui")
pin = uic.loadUi("Janelas/pin.ui")
all_logs = uic.loadUi("Janelas/all_logs.ui")
user_some_logs = uic.loadUi("Janelas/user_some_logs.ui")
pag_2_way = uic.loadUi("Janelas/2_way.ui")

### botoes ###

# botoes do home
home.pushButton.clicked.connect(abre_unlock)
home.pushButton_2.clicked.connect(abre_login)
home.pushButton_3.clicked.connect(exit)

# botoes do login
login.pushButton_4.clicked.connect(entrar_login)
login.pushButton_3.clicked.connect(abre_home)
login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

# botoes do root
root.pushButton_3.clicked.connect(abre_login)
root.pushButton_4.clicked.connect(abre_new_user)
root.pushButton_50.clicked.connect(todos_users)
root.pushButton_51.clicked.connect(todos_logs)
root.pushButton_2.clicked.connect(some_logs)

# botoes do new_user
new_user.pushButton_3.clicked.connect(voltar_new_user)
new_user.pushButton_4.clicked.connect(submeter_new_user)
new_user.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)

# botoes do all_users
all_users.pushButton_3.clicked.connect(voltar_all_users)
all_users.pushButton_4.clicked.connect(apagar_user)

# botoes do PIN
pin.pushButton_3.clicked.connect(pin_to_home) 
pin.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

# botoes do user_area
user_area.pushButton_3.clicked.connect(voltar_login)

# botoes do all_logs
all_logs.pushButton_3.clicked.connect(voltar_root)

# botoes do user_some_logs
user_some_logs.pushButton_3.clicked.connect(voltar_root_2)

# botoes do 2_way
pag_2_way.pushButton_3.clicked.connect(pag_2_way_to_home)

home.show()
app.exec()

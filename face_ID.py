import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import mysql.connector

data = mysql.connector.connect(
    host="LocalHost",
    user="root",
    passwd="",
    database="users"
)

path = "testes face id\Face_Recognition\Data_Base_fotos" #local onde as imagens dos users estao guardadas
imagens = [] # lista de imagens
nomes = [] #lista de nomes

lista_nome = os.listdir(path)



for cl in lista_nome:
    curimg = cv2.imread(f'{path}/{cl}') #ler as imagens no path
    imagens.append(curimg) #inserir as imagens na lista imagens
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
    success, img = cap.read() #ler o que esta a aparecer na camera
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) #fazer o resize da imagem (mete-la mais pequena)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #passar as imagens de RGB para BGR

    face_frame = face_recognition.face_locations(imgS) #encontar a localização das caras na imagem
    encode_frame = face_recognition.face_encodings(imgS, face_frame)

    for encodeframe, faceloc in zip(encode_frame, face_frame):
        matches = face_recognition.compare_faces(encodelistKnown, encodeframe)
        face_dis = face_recognition.face_distance(encodelistKnown, encodeframe)
        #print(face_dis)

        matcheIndex = np.argmin(face_dis) #fazer o match entre o valores do face_dis com os nomes

        if matches[matcheIndex]: #fazer o reconhecimento
            nome_ecra = nomes[matcheIndex].upper()

            y1,x2,y2,x1 = faceloc

            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2) #caixa a volta da cara 
            cv2.putText(img, nome_ecra, (x1+6,y2+26), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255), 2) #nome da pessoa

            print("Done", nome_ecra)

        else:
            nome_ecra = "UNKNOWN"

            y1,x2,y2,x1 = faceloc
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2) #caixa a volta da cara 
            cv2.putText(img, nome_ecra, (x1+6,y2+26), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2) #nome da pessoa

    cv2.imshow('Webcam', img) #mostrar imagem da camera
    cv2.waitKey(1)  

    if cv2.waitKey(20) & 0xFF == ord('q'):  # fechar a janela clicando na tecla "q"
        break

cap.release()
cv2.destroyAllWindows()

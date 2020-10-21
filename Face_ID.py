import cv2
import numpy as np
import face_recognition
import os
import re
import sys


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

i = 0
a = 0

while True:

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
            print(nome_ecra,i)

            #fazer aparecer retangulos na cara das pessoas
            y1,x2,y2,x1 = faceloc
            cv2.rectangle(imagem,(x1,y1),(x2,y2),(0,255,0),2) #caixa a volta da cara 
            cv2.putText(imagem, nome_ecra, (x1+6,y2+26), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255), 2) #nome da pessoa

            i = i + 1

        else:
            pass
            nome_ecra = "UNKNOWN"
            y1,x2,y2,x1 = faceloc
            cv2.rectangle(imagem,(x1,y1),(x2,y2),(0,0,255),2) #caixa a volta da cara 
            cv2.putText(imagem, nome_ecra, (x1+6,y2+26), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2) #nome da pessoa
            print(nome_ecra,a)
            
            a = a + 1
      
    cv2.imshow("Webcam", imagem)
            

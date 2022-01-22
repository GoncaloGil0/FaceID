import numpy as np
import cv2 
import os

face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')

cap = cv2.VideoCapture(1) #seleciona a camera, neste momento esta a default

folder_name = input("Folder name: ")

path = os.path.join("Face_id_fotos/", folder_name)

os.mkdir(path)

i = 0

while True:
    ret, frame = cap.read() #ler frame por frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #para conseguir o reconhecimento a frame tem de estar em gray (seguindo a documentação)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) #defenir a escala da frame, quando maior mais preciso´

    for (x, y, w, h) in faces:
        #print(x, y, w, h)

        roi_gray = gray[y:y+h, x:x+w] #(y=y+altura x=x+cumprimento)
        roi_color = frame[y:y+h, x:x+w]
       
        i = i +1


        #PRETO E BRANCO:
        img_nome = "Face_id_fotos/{}/my-image_{}.png".format(folder_name,i) 
        cv2.imwrite(img_nome, roi_gray)

        #CORES:
        #img_nome_cores = "Face_id_fotos/{}/my-image_color_{}.png".format(folder_name,i)
        #cv2.imwrite(img_nome_cores, roi_color)
        
        #desenhar um retangulo a volta da cara 
        color = (0, 255, 0) #BGR blue-green-red não é RGB
        stroke = 2 #tamanho da borda
        fim_x = x + w
        fim_y = y + h
        cv2.rectangle(frame, (x, y), (fim_x, fim_y), color, stroke)

    
    cv2.imshow('frame', frame) #mostrar a imagem

    if cv2.waitKey(20) & 0xFF == ord('q'): #fechar a janela clicando na tecla "q"
        break 

    if i == 200 :
        break

cap.release()
cv2.destroyAllWindows()
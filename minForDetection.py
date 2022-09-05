import cv2
import mediapipe as mp 
import time


cap = cv2.VideoCapture(0) 



mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDrawn = mp.solutions.drawing_utils


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) #rotira snjimak kao u ogledalu radi lakse orijentacije
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)#imgRGB se ne prikazuje samo se koristi za 
    results = hands.process(imgRGB) #funkcija proces koristi RGB zato moramo da pretvorimo

    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):#vraca id i lokacija tog dela ruke/tog ig 
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)#DAJE NAM POZICIJU ODREDJENIH ID 
                if id == 8:
                    print(id,lm)
                    cv2.circle(img,(cx,cy) , 10,(255,0,0), cv2.FILLED)#OZNAKA ZA PRST KOJI NAS ZANIMA
            mpDrawn.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)#kordinate koje dobije preslikavamo na img(crvene tackice 21 na kljucna mesta)
                                        #mpHands.HAND_CONNECTIONS - FUNKCIJA KOJA CRTA LINIJE IZMEDJU TACKICA




    cv2.imshow("Kamera",img)
    cv2.waitKey(1)
import cv2
import mediapipe as mp
import pyautogui
import time 
import os


#DETEKCIJA RUKE============================
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
#==========================================
x17 = 0
y17 = 0
x5 = 0
y5 = 0

move = 0

pTime = 0

lastclick = time.time()
click = 0

x16 = 0
y16 = 0

x12 = 0
y12 = 0 

y8 = 0
key=0
#GLAVNI LOOP===============================
while True:
    #DETEKCIJA RUKE NA RGB SLICI  I OBELIZIVANJE RUKE
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    #================================================

    if hands:#ovde ulazi ako je hands razlicit od nul
        for hand in hands:
            #CRTANJE TACAKA NA ODREDJENA MESTA RUKE
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                #=======================================
                #===========DISTANCE====================
                #=======================================
                if id == 17:
                    x17 = screen_width/frame_width*x 
                    y17 = screen_height/frame_height*y 

                if id == 5:
                    x5 = screen_width/frame_width*x
                    y5 = screen_height/frame_height*y 
                    distance_5_17 = ((y5-y17)**2 + (x5-x17)**2)**0.5
                    if distance_5_17 >320:
                        cv2.putText(frame,("ODALJI RUKU") , (20,40) , cv2.FONT_HERSHEY_PLAIN , 3, (0,0,0),3)
                        move = 1
                        
                    elif distance_5_17 < 150:
                        cv2.putText(frame,("PRIBLIZI RUKU") , (20,40) , cv2.FONT_HERSHEY_PLAIN , 3, (0,0,0),3)
                        move = 1
                    else:
                        move = 0
                #==============================================
                #==================move====================
                #==============================================
                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(0,0,0))
                    palac_x = screen_width/frame_width*x
                    palac_y = screen_height/frame_height*y
                #==============================================
                if id == 8:
                    #cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    x8 = screen_width/frame_width*x
                    y8 = screen_height/frame_height*y

                    distanceKaziprstPalac= ((y8 - palac_y)**2 + (x8 - palac_x)**2)**0.5


                    if distanceKaziprstPalac<50:
                        cureentlitime = time.time()

                        if cureentlitime - lastclick > 1.5:
                            click = 0
                        
                        cureentlitime = time.time()
                        if click == 0:
                            lastclick = cureentlitime
                            click = 1
                            pyautogui.click()                                
                            print("leftclick")
                            pyautogui.sleep(0.1) 

                        if click == 1 and cureentlitime - lastclick  > 0.3:
                            lastclick = cureentlitime
                            click = 0
                            pyautogui.click() 
                            pyautogui.sleep(1)                               
                            print("drugi left click")

                        
                    elif abs(y8 - y8) < 330 and move == 0: 
                        pyautogui.moveTo(palac_x, palac_y)
                #===========================================================
                #========right click ========================================
                if id == 12:
                    #cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))

                    x12 = screen_width/frame_width*x
                    y12 = screen_height/frame_height*y

                    distanceSrednjiPalac = ((y12 - palac_y)**2 + (x12 - palac_x)**2)**0.5
                    
                    if distanceSrednjiPalac < 40:
                        pyautogui.click(button='right')
                        pyautogui.sleep(0.5)
                        print("rightclick")
                #===========================================================
                #=================SKLOPLJENA SAKA =============================
                if id == 9: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0,0,0))
                    centar_x = screen_width/frame_width*x
                    centar_y = screen_height/frame_height*y
                    #print(centar_y)
                    #print(y12)
                    if y12 > centar_y+ 40 and key== 0:
                        os.system("On-Screen Keyboard")
                        key= 1 

                #==========================================================
                #===================BACK ZAMAHOM===========================
                if id == 20:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(30,144,255))
                    mali_x = screen_width/frame_width*x

                    if mali_x+80 < centar_x:
                        pyautogui.keyDown('alt')
                        pyautogui.press('left')
                        pyautogui.keyUp('alt')
                        pyautogui.sleep(1)
                        print("back")
                #=========================================================
                #===============PALJENJE TASTATURE========================
                if id == 16:
                    x16 = screen_width/frame_width*x
                    y16 = screen_width/frame_width*y
                if id == 0:
                    donjiCentar_x = screen_width/frame_width*x
                    donjiCentar_y = screen_width/frame_width*y
                    if (y8-10) - donjiCentar_y>20:
                        print("nadole")
                        pyautogui.press('down')
                        pyautogui.press('down')
                        pyautogui.sleep(0.3)

    cTime = time.time()
    fps = 1/(cTime - pTime)  
    pTime = cTime
    cv2.putText(frame,str(int(fps)) , (580,40) , cv2.FONT_HERSHEY_PLAIN , 3, (0,0,0),3) 
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)

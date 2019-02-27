# februarie 2019, Nitescu Radu, UPB Automatica si Calculatoare, ANUL 1
# radu.nitescu35@gmail.com
import cv2
import numpy
import time
import datetime
import serial
import RaduLCD
import base64
import pymongo
#afisare Data
def get_time( timp ):
    if timp.tm_mon == 1: luna = "January"
    elif timp.tm_mon == 2: luna = "February"
    elif timp.tm_mon == 3: luna = "March"
    elif timp.tm_mon == 4: luna = "April"
    elif timp.tm_mon == 5: luna = "May"
    elif timp.tm_mon == 6: luna = "June"
    elif timp.tm_mon == 7: luna = "July"
    elif timp.tm_mon == 8: luna = "August"
    elif timp.tm_mon == 9: luna = "September"
    elif timp.tm_mon == 10: luna = "October"
    elif timp.tm_mon == 11: luna = "November"
    elif timp.tm_mon == 12: luna = "Decembrie"
    if timp.tm_hour < 10 : ora = '0'+ str(timp.tm_hour)
    else: ora = str(timp.tm_hour)
    return luna + ' ' + str(timp.tm_mday) + ', ' + ora + '.' + str(timp.tm_min)

#baza de date

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["UsersAndLogs"]
Users = mydb["Users"]
Logs = mydb["Logs"]
ser = serial.Serial('COM5', 9600, timeout=0)
while True:
        RaduLCD.printOnLCD("Apropiati cardul","de cititor")
        cod_rfid = str(ser.readline())
        cod_rfid = cod_rfid[3:14];
        if len(cod_rfid) > 2: #Daca ia codul rfid
            time.sleep(1)
            myquery = { "RFID": cod_rfid }
            rezultate_cautare = Users.find_one(myquery)
            if rezultate_cautare != None:
                RaduLCD.printOnLCD("Asezati-va in","fata camerei")
                time.sleep(2)
                cap = cv2.VideoCapture(0)
                face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                while(True):
                    ret, img = cap.read() #ia cate un frame pe rand
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # face imaginea grayscale
                    faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.05, minNeighbors=5) #primeste coordonatele fetelor si lungimile
                    RaduLCD.printOnLCD("Cautare fata...","")
                    if len(faces) != 0: #IFUL CU LUAREA POZEI, Upload in LOG, deschidere usa
                        localtime = time.localtime(time.time())
                        data_pozei = get_time(localtime)
                        numele_pozei = data_pozei + '.jpg'
                        cv2.imwrite(numele_pozei, img )
                        RaduLCD.printOnLCD("Img capturata", "cu succes!")
                        with open(numele_pozei, "rb") as imageFile:
                            poza_binar = base64.b64encode(imageFile.read())
                        intrare_logs = {
                        "data":data_pozei,
                        "Nume":rezultate_cautare["Nume"],
                        "Prenume":rezultate_cautare["Prenume"],
                        "CNP":rezultate_cautare["CNP"],
                        "Fotografie":poza_binar
                        }
                        inserat = Logs.insert_one(intrare_logs)
                        break
                cap.release()
                cv2.destroyAllWindows()
            else:
                RaduLCD.printOnLCD("Acces respins!","") #printurile sunt pe LCD 16x2. A se verifica nr de caractere pt fiecare rand
                time.sleep(3)

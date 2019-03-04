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
def get_time( timp ): #!!! Change it - dictionary
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
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)
ok = 1
while True:
        if ok == 1:
            RaduLCD.printOnLCD("Apropiati cardul","de cititor")
            ok = 0
        cod_rfid = str(ser.readline())
        cod_rfid = cod_rfid[3:14]
        print(cod_rfid)
        if len(cod_rfid)>2:
            time.sleep(1)
            myquery = { "RFID": cod_rfid }
            print(myquery)
            rezultate_cautare = Users.find_one(myquery)
            print(rezultate_cautare)
            if rezultate_cautare != None:
                print(rezultate_cautare)
                RaduLCD.printOnLCD("Asezati-va in","fata camerei!")
                ok = 1
                time.sleep(2)
                cap = cv2.VideoCapture(0)
                face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                timp_start =  time.localtime(time.time())
                minutul_inceperii = timp_start.tm_min
                RaduLCD.printOnLCD("Cautare fata..."," ")
                while(minutul_inceperii + 2 >= time.localtime(time.time()).tm_min):
                    ret, img = cap.read() #ia cate un frame pe rand
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # face imaginea grayscale
                    faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.05, minNeighbors=5) #primeste coordonatele fetelor si lungimile

                    #IFUL CU LUAREA POZEI, Upload in LOG, deschidere usa
                    if len(faces) != 0:
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
                        time.sleep(3)
                        RaduLCD.printOnLCD("Bun Venit",rezultate_cautare["Nume"][0] + ". " + rezultate_cautare["Prenume"])
                        time.sleep(3)
                        break
                cap.release()
                cv2.destroyAllWindows()
            else:
                RaduLCD.printOnLCD("Acces respins!","") #printurile sunt pe LCD 16x2. A se verifica nr de caractere pt fiecare rand
                time.sleep(3)
                ok = 1

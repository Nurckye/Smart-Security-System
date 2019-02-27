# Smart-Security-System
A security system made with Arduino Uno and Raspberry Pi 3. 
Parts used:
Arduino Uno
Raspberry Pi 3
RFID sensor
Webcam
16x2 LCD

Each registered user will have a RFID card. When used the system will require taking a picture of the user and it will wait until it detects a face. Then it will send an opening signal to the door wich will allow access in the facility and it will store the time and information of the person as well as the taken photo in a NoSQL database which can be a locally administered.

Software used:
Python, C, OpenCV, Mongo database and Leon Anavi's git repository for the 16x2 LCD controll.

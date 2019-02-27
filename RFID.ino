#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);   
  
void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
}
void loop() 
{
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
    return;
  if ( ! mfrc522.PICC_ReadCardSerial()) 
    return;
 
  String cardData= "";
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     cardData.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     cardData.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println(cardData);
  delay(2000);
  
} 

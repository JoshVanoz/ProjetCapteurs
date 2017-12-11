/*
 * The sketch here will make Leonardo exchange
 * data between the USB serial port and SIM808 module.
*/

#include "WISMO228.h"

#define SMS_SERV "33783106914"

// SMSSender sms(Serial, Serial1);
WISMO228 sms(&Serial1, 11);
int photocellPin = 0;

void setup() {
    Serial.begin(115200); //initialize Serial(i.e. USB port)
    Serial1.begin(9600); //initialize Serial1

    while(!Serial); // Wait for USB

    pinMode(LED_BUILTIN, OUTPUT);

    sms.init();
    
    sms.powerUp();

    digitalWrite(LED_BUILTIN, HIGH);

    initGPS();
}

void loop() {
    //If Serial1 receive data, print out to Serial
    while (Serial1.available()) {
        byte data = Serial1.read();
        Serial.write(data);
        if (detectSms(data)) {
            //Serial1.write(data);
            printMsg();
        }
    }
    //If Serial receive data, print out to Serial1
    while (Serial.available()) {
        byte data = Serial.read();
        Serial.write(data);

        if (data == '*')
            digitalWrite(LED_BUILTIN, HIGH);
        else if (data == '-')
            digitalWrite(LED_BUILTIN, LOW);
        else if (data == '@')
            sms.sendSms(SMS_SERV, sense());
        else if (data == '%')
            sms.sendSms(SMS_SERV, readGPS());
        else
            Serial1.write(data);

    }
    delay(1);  //delay for a short time to avoid unstable USB communication
}

char* sense() {
    char charBuf[50];
    char ans[50];
    strcpy(ans, "Capteur : ");
    String(analogRead(photocellPin)).toCharArray(charBuf, 50);
    strcat(ans, charBuf);
    Serial.write(ans);
    return ans;
}

void flushSerial(Stream& s) {
  unsigned long now = millis ();
  while (millis () - now < 1000)
    s.read ();  // read and discard any input
}

void printMsg(void) {
    flushSerial(Serial1);
    char senderBuffer[RESPONSE_LENGTH_MAX];
    char contentBuffer[SMS_LENGTH_MAX];
    sms.readSms(senderBuffer, contentBuffer);
    Serial.print("Message de ");
    Serial.print(senderBuffer);
    Serial.print(" : ");
    Serial.println(contentBuffer);
}

int smsDetectionIndex = 0;
String smsDetectionExpect = "+CMTI: \"SM\",";

bool detectSms(char data) {
    if (smsDetectionIndex >= smsDetectionExpect.length()) {
        if (data == '\n') {
            smsDetectionIndex = 0;
            return true;
        }
    }
    else {
        if (data == smsDetectionExpect.charAt(smsDetectionIndex)) {
            smsDetectionIndex++;
        } else {
            smsDetectionIndex = 0;
        }
    }
    return false;
}

void initGPS() {
  Serial.println("Initialisation du GPS ...");
  Serial1.println("AT+CGNSPWR=1");
}

char* readLine(Stream &print) {
  // from sms
  Stream* printer = &print;
  delay(1);
  char lastChar = ' ';
  char* ans = "";
  while(printer->available() && lastChar != '\n') {
    lastChar = printer->read();
    ans += lastChar;
  }
  delay(1);
  return ans;
}

#define FRAM_LEN 200


char* readGPS() {
//  Serial.write("Sending request to GPS ... ");
//  Serial1.write("AT+CGNSINF\n");
  String raws = sendData("AT+CGNSINF\n", 1000, true);
//  Serial.write("Done.\n");
  char ans[24];
  char frame[FRAM_LEN];
  raws.toCharArray(frame, FRAM_LEN);
//  Serial.write("Raw : ");
//  Serial.print(frame);
//  Serial.write("\n---\n");
  strtok(frame, " ");
  strtok(NULL, ",");// Gets GNSSrunstatus
  strtok(NULL, ","); // Gets Fix status
  strtok(NULL, ","); // Gets UTC date and time
  strcpy(ans, "Position : ");
  strcat(ans, strtok(NULL, ",")); // Gets latitude
  strcat(ans, ";");
  strcat(ans, strtok(NULL, ",")); // Gets longitude
//  Serial.write("Extracted response : ");
  Serial.write(ans);
//  Serial.write("\n---\n");
  return ans;
}

String sendData(String command, const int timeout, boolean debug) {
    String response = "";    
    Serial1.println(command); 
    delay(5);
    long int time = millis();   
    while( (time+timeout) > millis()){
      while(Serial1.available()){       
        response += char(Serial1.read());
      }  
    }    
    if (debug) Serial.print(response);
    return response;
}


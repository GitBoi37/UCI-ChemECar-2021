#include <EEPROM.h>

unsigned long startTime;
float t;
bool moving = 0;
float endTime = 180;


int Relay = 3;
//for button
const int button_pin = 2;
//runs once when the arduino turns on
void setup() {
  pinMode(button_pin, INPUT);
  pinMode(Relay, OUTPUT);
  Serial.begin(115200); 
}

//runs repeatedly until time = 180 seconds
void loop() {
  int pinValue;
  pinValue = digitalRead(button_pin);
  //read pinValue to determine if button has been pressed
  if(pinValue == HIGH){
    delay(150);
    startTime = millis();
    //once the button has been pressed do loop code until t > endTime
    t = float(millis() - startTime)/float(1000);
    while(t < endTime){
      if(moving == 0){
        digitalWrite(Relay, HIGH);
      }
      moving = 1;
      Serial.print("t = ");
      Serial.println(t);
      delay(100);
      t = float(millis() - startTime)/float(1000);
      pinValue = digitalRead(button_pin);
      if(pinValue == HIGH){
        Serial.print("Eject button pressed, stopping car");
        break;
      }
    }
    moving = 0;
    Serial.print("Final time: ");
    Serial.print(t);
    Serial.println(" ENDPOINT REACHED! Resetting");
    digitalWrite(Relay, LOW);
    delay(250);
  }
}

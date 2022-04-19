#include "DFRobot_EC.h"
#include <EEPROM.h>

#define EC_PIN A1

//for ec probe
float voltage,ecValue,temperature = 25;
DFRobot_EC ec;
float endrange = 0.05;
float targetValue = 3;
unsigned long timeToWait = 5000; //5 seconds


//for button
const int button_pin = 2;

//for relay
int Relay = 3;


//runs once when the arduino turns on
void setup() {
  pinMode(button_pin, INPUT);
  pinMode(Relay, OUTPUT);
  Serial.begin(115200); 
}

//runs repeatedly until turned off
void loop() {
  int pinValue;
  pinValue = digitalRead(button_pin);
  //read pinValue to determine if button has been pressed
  if(pinValue == HIGH){
    //once the button has been pressed do loop code until some condition is met
    delay(250);
    delay(timeToWait);
    Serial.print("Button pushed, checking conductivity: ");
    while(abs(targetValue - ecValue) > endrange){
      digitalWrite(Relay, HIGH);
      voltage = analogRead(EC_PIN)/1024.0*5000;
      ecValue = ec.readEC(voltage,temperature);
      Serial.print(ecValue);
      Serial.println("ms/cm");
      delay(100);
      pinValue = digitalRead(button_pin);
      if(pinValue == HIGH){
        Serial.println("Eject button pressed");
        break;
      }
    }
    Serial.println("ENDPOINT REACHED! Resetting...");
    digitalWrite(Relay, LOW);
    delay(250);
  }
}

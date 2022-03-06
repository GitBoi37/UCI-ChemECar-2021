#include "DFRobot_EC.h"
#include <EEPROM.h>

#define EC_PIN A1

//for ec probe
float voltage,ecValue,temperature = 25;
DFRobot_EC ec;
float endrange = 0.05;

//for button
const int button_pin = 2;
//runs once when the arduino turns on
void setup() {
  pinMode(button_pin, INPUT);
  Serial.begin(115200); 
}

//runs repeatedly until turned off
void loop() {
  int pinValue;
  pinValue = digitalRead(button_pin);
  //read pinValue to determine if button has been pressed
  if(pinValue == HIGH){
    
    //once the button has been pressed do loop code until some condition is met
    //normally you would read the sensor value here in place of numloops
    while(abs(targetValue - ecValue) > endrange){
      voltage = analogRead(EC_PIN)/1024.0*5000;
      ecValue = ec.readEC(voltage,temperature);
      //also normally this would just be something like powermotor() or digitalpin(4, HIGH) to open a relay to power the motor
      Serial.print("Button pushed, checking conductivity: ");
      Serial.print(ec);
      Serial.println("ms/cm");
      delay(100);
    }
    Serial.println("ENDPOINT REACHED! Resetting");
  }
}

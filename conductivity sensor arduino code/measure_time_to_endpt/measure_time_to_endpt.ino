#include <DFRobot_EC.h>
#include "DFRobot_EC.h"
#include <EEPROM.h>
#define EC_PIN A1

/* Hello proud data collector!
 * This code is to be used to collect conductivity data with a static endpoint between trials
 * It'll stop once it reaches the endpoint hardcoded right below this but only if within +- range of it
 * It spits out a time anyways so if it skips over it just manually take the time and restart it or something
 * 
 */
float endpoint = 10.5;

float range = 0.05;

float voltage,ecValue,temperature = 25; //don't need to tweak these pretty sure
DFRobot_EC ec;
unsigned long startTime;
unsigned long thousand = 1000;
void setup()
{
  Serial.begin(115200);  
  ec.begin();
  startTime = millis();
}

void loop()
{
    Serial.println("Enter anything here to start data collection");
    while (Serial.available() <= 0)
    {}
    startTime = millis();
    while(1){
      static unsigned long timepoint = millis();
      if(millis()-timepoint>250U)  //time interval: 0.25s
      {
        timepoint = millis();
        voltage = analogRead(EC_PIN)/1024.0*5000;   // read the voltage
        //temperature = readTemperature();          // read your temperature sensor to execute temperature compensation
        ecValue =  ec.readEC(voltage,temperature);  // convert voltage to EC with temperature compensation
        Serial.print("temperature:");
        Serial.print(temperature,1);
        Serial.print("^C  EC:");
        Serial.print(ecValue,2);
        Serial.print("ms/cm Endpoint:");
        Serial.print(endpoint,2);
        Serial.print("ms/cm Delta: ");
        Serial.print(endpoint-ecValue);
        Serial.print("ms/cm Time: ");
        Serial.println(float((millis() - startTime))/float(thousand));
        //if value is within 0.05 range of endpoint then stop the loop
        if(abs(endpoint - ecValue) < range){
          Serial.print("Time to endpoint: ");
          Serial.println(float(millis() - startTime)/float(thousand));
          break;
        }
      } 
    }
    ec.calibration(voltage,temperature);          // calibration process by Serail CMD
}

float readTemperature()
{
  //add your code here to get the temperature from your temperature sensor
}

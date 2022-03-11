#include <DFRobot_EC.h>
#include "DFRobot_EC.h"
#include <EEPROM.h>

#define EC_PIN A1

/* Hello datanauts this code is meant to be used to rerun conductivity tests but with a varying endpoint on each trial
 * You don't have to set the endpoint manually unlike the other code, super helpful!
 * 
 */

float endpoint = 10.5; //you don't have to set this manually

float range = 0.05; //you can tweak this if you want, larger range is less precise but more able to account for rapid fluctuation


float voltage,ecValue,temperature = 25;
DFRobot_EC ec;
int x = 0;
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
    Serial.println("Enter endpoint here to start data collection");
    while (Serial.available() <= 0)
    {}
    endpoint = (Serial.parseFloat());
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

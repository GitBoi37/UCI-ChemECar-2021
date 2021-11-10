#include <DFRobot_TCS34725.h>
#include "DFRobot_TCS34725.h"
/*This file utilizes the DFRobot library to 
  interface the TCS34725 library, look at the library headers for
  things to use */

//pins:
//Green Wire = A4
//Blue Wire = A5
//Black Wire = GND
//Red Wire = 5V
//integration time is 154ms
// 2_4,    24,    50,   101,   154,   700 | possible times (ms)
//1024, 10240, 20480, 43008, 65358, 65358 | max count
//higher integration time is more accurate but refreshes slower
DFRobot_TCS34725 tcs = DFRobot_TCS34725(TCS34725_INTEGRATIONTIME_154MS, TCS34725_GAIN_4X);

void setup() {
  //must set baud to 9600 in the serial monitor!
  Serial.begin(9600);
  Serial.println("Color View Test!");
  //if sensor is on then do things else, halt
  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1); // halt!
  }
}
 
void loop() {
  //c is the sum of all 3 i think, RGB are self-explanatory
  //see above for max values depending on integration time
  uint16_t c, red, green, blue, colorTemperature, lux;
  tcs.getRGBC(&red, &green, &blue, &c); //get RGB and C
  tcs.lock();  // turn off LED (doesn't work on the new sensors)
  colorTemperature = tcs.calculateColorTemperature(red, green, blue); //calculate color temperature
  lux = tcs.calculateLux(red, green, blue); //calculate lux
  //output should look like:
  //colorTemperature,lux,c,rawRed,rawGreen,rawBlue,R,G,B
  Serial.print(colorTemperature);
  Serial.print(","); Serial.print(lux);
  Serial.print(","); Serial.print(c);
  Serial.print(","); Serial.print(red);
  Serial.print(","); Serial.print(green);
  Serial.print(","); Serial.print(blue);
  uint32_t sum = c;
  float r,g,b;
  r = red; r /= sum;
  g = green; g /= sum;
  b = blue; b /= sum;
  r *= 256; g *= 256; b *= 256;
  Serial.print(","); Serial.print(r);
  Serial.print(","); Serial.print(g);
  Serial.print(","); Serial.print(b);
  Serial.println();
}

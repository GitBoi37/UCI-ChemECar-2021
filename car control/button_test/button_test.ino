const int button_pin = 7;
int numLoops = 1;
int targeetValue = 10;
//runs once when the arduino turns on
void setup() {
  pinMode(button_pin, INPUT);
}

//runs repeatedly until turned off
void loop() {
  int pinValue;
  pinValue = digitalRead(button_pin);
  Serial.println(pinValue);
  if(pinValue == 1){
    //normally you would read the sensor value here in place of numloops
    while(numLoops < targetValue){
      //also normally this would just be something like powermotor() or digitalpin(4, HIGH) to open a relay to power the motor
      Serial.println("Looped through " + numLoops + " times");
    }
  }
}

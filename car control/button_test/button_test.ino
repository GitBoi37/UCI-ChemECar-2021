const int button_pin = 2;
int numLoops = 1;
int targetValue = 10;
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
    while(numLoops < targetValue){
      //also normally this would just be something like powermotor() or digitalpin(4, HIGH) to open a relay to power the motor
      Serial.print("Looped through ");
      Serial.print(numLoops);
      Serial.println(" times");
      numLoops += 1;
      delay(500);
    }
    numLoops = 0;
  }
}

int springPins[] = {5,6};
void setup() {
  // initialize digital SMA spring pins (iterate through ledPins) as an output and button pin as an input
  for (int i = 0; i < 2; i++){
    pinMode(springPins[i], OUTPUT);
    digitalWrite(springPins[i], LOW);
  }

  // set baud rate for serial communication
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(springPins[0], HIGH);
//  delay(5000);
//  Serial.println(digitalRead(springPins[0]));
//  digitalWrite(springPins[0], LOW);  
//  delay(5000); 
//  Serial.println(digitalRead(springPins[0])); 
  //exit(0);
}

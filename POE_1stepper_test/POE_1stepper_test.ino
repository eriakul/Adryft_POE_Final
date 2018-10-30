//#include <AccelStepper.h>
//#include <SpeedyStepper.h>
//
//// Create AccelStepper object for stepper driver with Step and Direction pins
//AccelStepper Xaxis(1, 54, 55); // pin 54 = step, pin 55 = direction
//AccelStepper Yaxis(1, 60, 61); // pin 60 = step, pin 61 = direction
//
//void setup() {
//  // put your setup code here, to run once:
//  Serial.begin(9600);           // set up Serial library at 9600 bps
//  Serial.println("Stepper test!");
//  // set stepper motor speeds
//  Xaxis.setSpeed(50);
//  Xaxis.moveTo(100); 
//  //Yaxis.setSpeed(50);
//  //Yaxis.moveTo(100); 
//}
//
//void loop() {
//  // put your main code here, to run repeatedly:
//  Serial.println(Xaxis.distanceToGo());
//  Xaxis.runSpeed();
//  //Serial.println(Yaxis.distanceToGo());
//  //Yaxis.runSpeed();
//}

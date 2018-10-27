#include <AccelStepper.h>
#include <AFMotor.h>

AF_Stepper motor1(200, 2);
//200 indicates how many steps per revolution the motor has. A 7.5 degree/step motor has 360/7.5 = 48 steps.
//2 is which port it is connected to. If you're using M1 and M2, its port 1. If you're using M3 and M4 indicate port 2

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// another potential function to use step(#steps, direction, steptype)
void forwardstep() {  
  motor1.step(1, FORWARD, SINGLE);
}
void backwardstep() {  
  motor1.step(1, BACKWARD, SINGLE);
}

AccelStepper stepper(forwardstep, backwardstep); // use functions to step

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");
  // set stepper motor speeds
  stepper.setSpeed(50);
  stepper.move(24);  
}

void loop() {
  // put your main code here, to run repeatedly:
  stepper.runSpeed();
}

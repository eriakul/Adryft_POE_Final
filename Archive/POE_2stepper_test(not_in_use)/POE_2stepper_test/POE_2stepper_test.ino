#include <AccelStepper.h>
#include <AFMotor.h>


// two stepper motors one on each port
AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void forwardstep1() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  motor1.onestep(BACKWARD, SINGLE);
}
// wrappers for the second motor!
void forwardstep2() {  
  motor2.onestep(FORWARD, SINGLE);
}
void backwardstep2() {  
  motor2.onestep(BACKWARD, SINGLE);
}

// Motor shield has two motor ports, now we'll wrap them in an AccelStepper object
AccelStepper stepper1(forwardstep1, backwardstep1);
AccelStepper stepper2(forwardstep2, backwardstep2);

void setup()
{  
    stepper1.setSpeed(50);
    //stepper1.setAcceleration(100.0);
    stepper1.moveTo(24);
    
    stepper2.setSpeed(50);
    //stepper2.setAcceleration(100.0);
    stepper2.moveTo(24);
    
}

void loop()
{
    // Change direction at the limits
    Serial.println(stepper1.distanceToGo());
    if (stepper1.distanceToGo() == 0)
  stepper1.moveTo(-stepper1.currentPosition());
    stepper1.runSpeed();
    stepper2.runSpeed();
    
    //stepper2 blocking (set target position and wait until motor achieves it)
    //stepper2.runToNewPosition(0);
    //stepper2.runToNewPosition(500);
    //stepper2.runToNewPosition(100);
    //stepper2.runToNewPosition(120);
    // there are also examples for overshoot testing
}

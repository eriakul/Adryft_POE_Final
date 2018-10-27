#include <AccelStepper.h>
#include <AFMotor.h>

// two stepper motors one on each port
AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);
const float GEAR_RATIO = -5;
const float DEG_PER_STEP = 1.8;
float Current_Pos = 0; 
String readString;
String radius1;
String theta1;
float radius2;
float theta2;

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

float moveStep(float r, float t){
  float numStep = t/(DEG_PER_STEP/GEAR_RATIO);
  return numStep;
}

void wrapString(){
  // function to call the top motor to wrap string around the peg
}

void setup()
{  
    //stepper1.setMaxSpeed(200.0);
    //stepper1.setAcceleration(100.0);
    //stepper1.moveTo(24);
    //stepper2.setMaxSpeed(300.0);
    //stepper2.setAcceleration(100.0);
    //stepper2.moveTo(1000000);
    stepper1.setSpeed(50);
    stepper2.setSpeed(50);
    Serial.begin(9600);
    
}

void loop()
{
  while(!Serial.available()) {}
  // serial read section
  while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      readString = Serial.readString();
      int commaIndex = readString.indexOf(',');
      radius1 = readString.substring(0, commaIndex);
      theta1 = readString.substring(commaIndex + 1);
      radius2 = radius1.toFloat();
      theta2 = theta1.toFloat();
      stepper1.moveTo(moveStep(radius2, theta2));
      while (stepper1.distanceToGo()>0){
        stepper1.runSpeed();
      }
      wrapString();
    }
  }

  

  if (readString.length() >0)
  {
    Serial.print("Arduino received: ");  
    String radius3 = String(radius2*2);
    String theta3 = String(theta2*2);
    Serial.print(radius3); //see what was received
    Serial.print(",");
    Serial.println(theta3);
  }
  delay(500);
  Serial.flush();
}

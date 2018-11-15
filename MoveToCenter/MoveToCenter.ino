// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <SpeedyStepper.h>

const int MOTOR_STEP_PIN_T = 60; // for theta motor
const int MOTOR_DIRECTION_PIN_T = 61;
const int STEPPER_ENABLE_PIN_T = 56;
const int MOTOR_STEP_PIN_R = 46; // for radius motor
const int MOTOR_DIRECTION_PIN_R = 48;
const int STEPPER_ENABLE_PIN_R = 62;
const int R_LIMIT_SWITCH_OUTPUT = 32; 

// Create two adafruit stepper motors, one on each port
// Create AccelStepper object for stepper driver with Step and Direction pins
SpeedyStepper stepper_t;
SpeedyStepper stepper_r;

// Create constant variables regarding mechanical system and stepper deg/step
const int REV_TO_DEGREE = 360; // degrees in one revolution 
const float GEAR_RATIO = -4.69; // negative since gear spins opposite direction to motor
const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float FEET_TO_MM = 25.4*12; // multiply feet by this constant to get mm
const float STEPS_PER_MM = 100/1.25; // divide expected distance by constant to account for offset
//const float DEG_PER_STEP = 1.8; // obtained from NEMA stepper motor spec sheet
const float DEG_PER_PEG = 7.5; // degree per peg to wrap string around
const float RADIUS_IN_MM = 329.406; // distance from end of r axis to center

void setup()
{  
    // Set up stepper motors
    // theta = stepper_t
//    pinMode(STEPPER_ENABLE_PIN_T, OUTPUT);
//    digitalWrite(STEPPER_ENABLE_PIN_T,LOW);
//    stepper_t.connectToPins(MOTOR_STEP_PIN_T, MOTOR_DIRECTION_PIN_T);
    // radius = stepper_r
    pinMode(STEPPER_ENABLE_PIN_R, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_R,LOW);
    stepper_r.connectToPins(MOTOR_STEP_PIN_R, MOTOR_DIRECTION_PIN_R);

    //set up speed and acceleartion for stepper_t
//    stepper_t.setStepsPerRevolution(3200);
//    stepper_t.setSpeedInRevolutionsPerSecond(0.3);
//    stepper_t.setAccelerationInRevolutionsPerSecondPerSecond(0.3);

    //set up speed and acceleartion for stepper_r
    stepper_r.setStepsPerMillimeter(STEPS_PER_MM); // set the number of steps per millimeter
    stepper_r.setSpeedInMillimetersPerSecond(50); // set the speed in mm/sec
    stepper_r.setAccelerationInMillimetersPerSecondPerSecond(40); // set the acceleration in mm/sec^2
    delay(100);
    
    stepper_r.setupRelativeMoveInMillimeters(RADIUS_IN_MM/1.038); // move relative mm
    while(!stepper_r.motionComplete())
    {
      stepper_r.processMovement();
    }

    // home the motor by moving until the homing sensor is activated, then set the position to zero
//    pinMode(R_LIMIT_SWITCH_OUTPUT, INPUT);
//    Serial.println("HOMING");
//    stepper_r.moveToHomeInMillimeters(-1, 20, 250, R_LIMIT_SWITCH_OUTPUT);
//    Serial.println("Found Home");
    
    // Set up serial port
    Serial.begin(9600);  
    delay(30);
    Serial.println("done");
}

void loop() {
  // put your main code here, to run repeatedly:
  exit(0);
}

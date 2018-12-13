// Stepper_Control combines serial port communication and stepper motor control. This is our main arduino script. 
// Import stepper motor libraries
#include <SpeedyStepper.h>
#include <StackArray.h>

const int MOTOR_STEP_PIN_T = 60; // for theta motor
const int MOTOR_DIRECTION_PIN_T = 61;
const int STEPPER_ENABLE_PIN_T = 56;
const int MOTOR_STEP_PIN_R = 46; // for radius motor
const int MOTOR_DIRECTION_PIN_R = 48;
const int STEPPER_ENABLE_PIN_R = 62;
const int R_LIMIT_SWITCH_OUTPUT = 32; // digital pin of limit switch

// Create SppedyStepper object for stepper drivers with Step and Direction pins
SpeedyStepper stepper_t;
SpeedyStepper stepper_r;

// Create constant variables regarding mechanical system and conversion factors
const int DEGREE_TO_REV = 360; // degrees in one revolution 
const float GEAR_RATIO = -79/13*1.1429; // negative since gear spins opposite direction to motor
const float FEET_TO_MM = 25.4*12; // multiply feet by this constant to get mm
const float STEPS_PER_MM = 80; // not 100 to account for offset

// Create variables for computation
float NUM_PEGS = 96;
float WRAP_FACTOR = 0.08; // how much dispenser should go in/out when wrapping
float RADIUS = 1; // in feet
float DEG_PER_PEG = 360/NUM_PEGS; // how much dispenser should turn when wrapping
float CROSS_FACTOR = 1; // keeps track what side of pegboard dispenser is on (similar to N/S in previous versions)
float ACROSS_RADIUS = -1.83; // distance to move when crossing pegboard
int curr_peg_num = 0; // first peg always starts at 0

// Create variables for serial communication
String peg_list;
String peg_nums;
String move_types;
int peg_nums_arr[200];
int move_types_arr[200];
int first = 1; // used to move the dispenser to the edge before executing any commands

// Create stack arrays for unwind function 
StackArray<int> motor_types;
StackArray<float> commands;

// unWind() takes in the motor_types and commands stack arrays and keep executing the comands
// until the stacks are empty   
void unWind(StackArray<int> motor_types, StackArray<float> commands){
    while (!motor_types.isEmpty()){
      int motor_type = motor_types.pop();
      float command = commands.pop();
      if (motor_type == 0){ // motor_type of 0 means move theta motor
        stepper_t.setupRelativeMoveInRevolutions(command);
        while(!stepper_t.motionComplete())
        {
          stepper_t.processMovement();
        }
      }
      else{ // motor_type of 1 means move radius motor
        stepper_r.setupRelativeMoveInMillimeters(command);
        while(!stepper_r.motionComplete())
        {
          stepper_r.processMovement();
        }
      }
    }
}

// move_to_peg() takes in the target peg number and move_type
// Computations, wraps, and motor executions all occur in this function
void move_to_peg(int next_peg, int move_type){
  // Find current and next peg locations (in degrees)
  float next_peg_loc = (360/NUM_PEGS)* next_peg;
  float curr_peg_loc = (360/NUM_PEGS)* curr_peg_num;
  // Create dr and dtheta motor command variables
  float dr = 0;
  float dtheta = 0;
  // Find differences between next and current peg locations
  float diff1 = limitAngle2(next_peg_loc-curr_peg_loc);
  float diff2 = (360 - abs(diff1))*(diff1/abs(diff1));
  // Find the smallest difference between diff1 and diff2
  float min_diff1;
  if(abs(diff1) < abs(diff2)){
    min_diff1 = diff1;
  }
  else{
    min_diff1 = diff2;
  }
  // If move_type is 0 just wrap around to the new peg
  if(move_type == 0){ 
    dtheta = min_diff1;
    if(dtheta < 0){ // going CW (added after testing)
      // Shift dtheta and next_peg by one so the correct peg is wrapped around
      dtheta = dtheta - DEG_PER_PEG;  
      next_peg = next_peg - 1;
    }
    // Move by dtheta
    stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(dtheta));
    while(!stepper_t.motionComplete())
    {
      stepper_t.processMovement();
    }
    // Add motor command to stacks
    commands.push(-moveRevolutions(dtheta));
    motor_types.push(0);
  }
  // If move_type is 1 move across pegboard and wrap around peg
  // Main decision to be made is whether to cross the pegboard or not 
  else{
    // Find current peg location (in degress) if dispenser crosses pegboard
    float curr_peg_loc_across = limitAngle(curr_peg_loc-180);
    // Find differences between next and across current peg locations 
    float diff3 = limitAngle2(next_peg_loc-curr_peg_loc_across);
    float diff4 = (360 - abs(diff3))*(diff3/abs(diff3));
    // Find the smallest difference between diff3 and diff4
    float min_diff2;
    if(abs(diff3) < abs(diff4)){
      min_diff2 = diff3;
    }
    else{
      min_diff2 = diff4;
    }
    // Cross if both diff1 and diff2 > 90
    if (abs(min_diff1) > 90.0){
      // Set dtheta to smallest diff with curr_peg_loc_across
      dtheta = min_diff2;
      // Set dr to go across pegboard
      dr = CROSS_FACTOR*RADIUS*ACROSS_RADIUS; 
      // First move dispenser into pegboard so it can draw a line across 
      stepper_r.setupRelativeMoveInMillimeters(moveRadius(RADIUS*WRAP_FACTOR*CROSS_FACTOR));
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
      // Add motor command to stacks
      commands.push(-moveRadius(RADIUS*WRAP_FACTOR*CROSS_FACTOR));
      motor_types.push(1);
      // Move by dtheta and dr (both motor move concurrently)
      stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(dtheta));
      stepper_r.setupRelativeMoveInMillimeters(-moveRadius(dr)); // neg accounts for direction
      while(!stepper_t.motionComplete()||!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
        stepper_t.processMovement();
      }
      // Add motor commands to stacks
      commands.push(-moveRevolutions(dtheta));
      motor_types.push(0);
      commands.push(moveRadius(dr));
      motor_types.push(1);      
      // Adjust CROSS_FACTOR after crossing
      CROSS_FACTOR = -1*CROSS_FACTOR;
      // Wrap around peg 
      wrapAround(CROSS_FACTOR);
    }
    // If either diff1 or diff2 < 90, don't cross
    else {
      // Set dtheta to smallest diff with curr_peg_loc
      dtheta = min_diff1;
      // Set dr to zero since not crossing
      dr = 0;
      // First move dispenser into pegboard so it can draw a line across
      stepper_r.setupRelativeMoveInMillimeters(moveRadius(RADIUS*WRAP_FACTOR*CROSS_FACTOR));
      while(!stepper_r.motionComplete())
      {
        stepper_r.processMovement();
      }
      // Add motor command to stacks
      commands.push(-moveRadius(RADIUS*WRAP_FACTOR*CROSS_FACTOR));
      motor_types.push(1);
      // Move by dtheta
      stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(dtheta));
      while(!stepper_t.motionComplete())
      {
        stepper_t.processMovement();
      }
      // Add motor command to stacks
      commands.push(-moveRevolutions(dtheta));
      motor_types.push(0);
      // Wrap around peg
      wrapAround(CROSS_FACTOR);
    }   
  }
  // Update current peg number
  curr_peg_num = next_peg;
}

// limitAngle makes sure an inputted angle is between the range (0, 360)
float limitAngle(float angle){
  if(angle < 0){
    angle = angle + 360;
  }
  else if(angle > 360){
    angle = angle - 360;
  }
  return angle;
}

// limitAngle2 makes sure abs(angle) is between the range (0, 36)
float limitAngle2(float angle){
  if(abs(angle) > 360){
    if(angle > 0){
      angle = angle - 360;
    }
    else{
      angle = angle + 360;
    }
  }
  return angle;
}

// wrapAround takes an inputed direction and uses it to execute a series of 5 motor commands
void wrapAround(float dir){
  // dir is the CROSS_FACTOR. 1 means dispenser is on the same side as the limit switch (-1 indicate the opp side) 
  // Increase motor speed when wrapping 
  stepper_t.setSpeedInRevolutionsPerSecond(2);
  stepper_t.setAccelerationInRevolutionsPerSecondPerSecond(2);
  stepper_r.setSpeedInMillimetersPerSecond(200); 
  stepper_r.setAccelerationInMillimetersPerSecondPerSecond(250); 
  // 1) Move dispenser to edge of pegboard (move out)
  stepper_r.setupRelativeMoveInMillimeters(-dir*moveRadius(RADIUS*WRAP_FACTOR)); 
  while(!stepper_r.motionComplete())
  {
    stepper_r.processMovement();
  }
  // 2) Move dispenser clockwise by one peg
  stepper_t.setupRelativeMoveInRevolutions(-moveRevolutions(DEG_PER_PEG));  
  while(!stepper_t.motionComplete())
  {
    stepper_t.processMovement();
  }
  // 3) Move dispenser into pegboard (opposite of 1)
  stepper_r.setupRelativeMoveInMillimeters(dir*moveRadius(RADIUS*WRAP_FACTOR));
  while(!stepper_r.motionComplete())
  {
    stepper_r.processMovement();
  }
  // 4) Move dispenser counter clockwise by one peg (opposite of 2)
  stepper_t.setupRelativeMoveInRevolutions(moveRevolutions(DEG_PER_PEG)); 
  while(!stepper_t.motionComplete())
  {
   stepper_t.processMovement();
  }
  // 5) Move dispenser back to edge of board (same as 1)
  stepper_r.setupRelativeMoveInMillimeters(-dir*moveRadius(RADIUS*WRAP_FACTOR)); 
  while(!stepper_r.motionComplete())
  {
    stepper_r.processMovement();
  }
  // Add motor commands to stacks
  commands.push(dir*moveRadius(RADIUS*WRAP_FACTOR));
  motor_types.push(1);
  commands.push(moveRevolutions(DEG_PER_PEG));
  motor_types.push(0);
  commands.push(-dir*moveRadius(RADIUS*WRAP_FACTOR));
  motor_types.push(1);
  commands.push(-moveRevolutions(DEG_PER_PEG));
  motor_types.push(0);
  commands.push(dir*moveRadius(RADIUS*WRAP_FACTOR));
  motor_types.push(1);
  // Reset motor speeds
  stepper_t.setSpeedInRevolutionsPerSecond(0.8);
  stepper_t.setAccelerationInRevolutionsPerSecondPerSecond(0.8);
  stepper_r.setSpeedInMillimetersPerSecond(150); 
  stepper_r.setAccelerationInMillimetersPerSecondPerSecond(170);
}

// toEdge moves the dispense to the starting position a few mm in front of the limit switch 
// Called once after calibration 
void toEdge(){
    // Move radius motor in by 10mm
    stepper_r.setupRelativeMoveInMillimeters(10);
    while(!stepper_r.motionComplete())
    {
      stepper_r.processMovement();
    }
}

// moveRevolutions takes in a theta value and calculates how many relative revolutions stepper_t should make 
float moveRevolutions(float theta){
  // Multiply theta by gear ratio to make sure pegboard rotates by theta
  float numRevo = theta/(DEGREE_TO_REV/GEAR_RATIO);
  return numRevo;
}

// moveRadius takes in a radius value (in feet) and calculates how many mms stepper_r should move
float moveRadius(float radius){
  // 1.038 is an offset value determined experimentalyl
  return (radius*FEET_TO_MM/1.038);
}

// setup initializes the stepper motors, limit switch, serial port, and runs the limit switch calibration
void setup()
{  
    // Set up theta stepper motor
    pinMode(STEPPER_ENABLE_PIN_T, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_T,LOW);
    stepper_t.connectToPins(MOTOR_STEP_PIN_T, MOTOR_DIRECTION_PIN_T);
    // Set up radius stepper motor
    pinMode(STEPPER_ENABLE_PIN_R, OUTPUT);
    digitalWrite(STEPPER_ENABLE_PIN_R,LOW);
    stepper_r.connectToPins(MOTOR_STEP_PIN_R, MOTOR_DIRECTION_PIN_R);

    // Set up speed and acceleration for stepper_t
    stepper_t.setStepsPerRevolution(3200);
    stepper_t.setSpeedInRevolutionsPerSecond(0.8);
    stepper_t.setAccelerationInRevolutionsPerSecondPerSecond(0.8);

    // Set up speed and acceleration for stepper_r
    stepper_r.setStepsPerMillimeter(STEPS_PER_MM); 
    stepper_r.setSpeedInMillimetersPerSecond(150); 
    stepper_r.setAccelerationInMillimetersPerSecondPerSecond(170);

    // Set up serial port
    Serial.begin(9600);  

    // Setup limit switch
    pinMode(R_LIMIT_SWITCH_OUTPUT, INPUT_PULLUP);
    // Home the radius motor by moving until the homing sensor is activated
    stepper_r.moveToHomeInMillimeters(-1, 20, 250, R_LIMIT_SWITCH_OUTPUT);
}

// loop receives the peg list message from python, converts it into two arrays of floats
// Calls move_to_peg for every peg number and move_type
// Send return message when tasks completed and waits for reply 
void loop()
{
  // Do nothing if no message from python
  while(!Serial.available()) {} 
  // Serial read section
  while(Serial.available()){
    delay(30);
    int index = 0; // keeps track of how many peg_num and move_type pairs are in peg_list
    if (Serial.available() > 0)
    {
      // Read in python message
      peg_list = Serial.readString();
      // If receive "Finished" message, then run unwind function 
      if(peg_list == "Finished"){
        delay(5000);
        unWind(motor_types,commands);
        exit(0);
      }
      int semiColonIndex = peg_list.indexOf(';'); // find index that separates peg_nums from move_types
      // Get string of peg_nums and move_types
      peg_nums = peg_list.substring(0, semiColonIndex);
      move_types = peg_list.substring(semiColonIndex+1);
      // Convert peg_nums and move_types to arrays of integers
      while(peg_nums.indexOf(',') != -1){
        int commaIndex_peg = peg_nums.indexOf(',');
        int commaIndex_move = move_types.indexOf(',');
        // Get next peg_num and move_type
        String temp_peg = peg_nums.substring(0, commaIndex_peg);
        String temp_move = move_types.substring(0, commaIndex_move);
        // Convert to ints and append to arrays
        peg_nums_arr[index] = temp_peg.toInt();
        move_types_arr[index] = temp_move.toInt();
        index = index+1;
        peg_nums = peg_nums.substring(commaIndex_peg+1);
        move_types = move_types.substring(commaIndex_move+1);
      }
      // Add in last command
      peg_nums_arr[index] = peg_nums.toInt();
      move_types_arr[index] = move_types.toInt();
      index = index + 1;
    }
 
    if (peg_list.length() > 0) 
    {
      peg_list = ""; // reset peg_list 
      if(first == 1){ // for just first time, move to the starting position
        toEdge();
        first = 0;
      }
      // Iterate through peg_nums_arr and move_types_arr, calling move_to_peg 
      for(int i=0; i< index; i++){
        move_to_peg(peg_nums_arr[i], move_types_arr[i]);
      }
      // Send reply message when tasks finished
      Serial.println("Tasks Completed!");
    }
    Serial.flush();
  }
}

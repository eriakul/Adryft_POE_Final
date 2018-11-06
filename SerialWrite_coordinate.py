# SerialWrite_coordinate

# Import libraries to connect python script with arduino serial monitor
import serial
import numpy as np
import re
import time

# NOTE: While this is running, you can not re-program the Arduino. You must exit
# this Python program before downloading a sketch to the Arduino.

# Set the name of the serial port
arduinoComPort = "COM7"

# Set the baud rate
# NOTE: The baudRate for the sending and receiving programs must be the same!
baudRate = 9600

# Open the serial port
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)
# Keep reading in each line in the Serial until the user initiates
# KeyboardInterrupt with CTRL-C
try:
  while True:
    # Write to serial port
    coordinate = [10, 3.1415]
    serialPort.flush()
    radius = str(coordinate[0])
    theta = str(coordinate[1])
    msg1 = radius + "," + theta
    msg1 = msg1.encode()
    print("Python value sent: ")
    print(msg1)
    serialPort.write(msg1)
    time.sleep(1)

    # Serial read section
    msg = serialPort.readline().decode()
    print ("Message from arduino: ")
    print (msg)

# Completed when CTRL-C pressed
except KeyboardInterrupt:
  print("Completed!")
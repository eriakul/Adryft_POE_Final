# serial_communication is in charge of taking a peg list and sending it to the
# Arduino script through serial port communication

# Import necessary libraries
import sys
import time
import serial

def send_list_and_receive_response(peg_list, serial_port):
    """
    send_list_and_receive_response converts a peg_list of tuples into a string
    peg_nums followed by their move_types

    peg_list: list of tuples in the format (peg_num, move_type)
    serial_port: Arduino serial port to send message to
    """
    no_response = True
    response = None
    serial_port.flush()
    # Make msg strings for peg_num and move_type
    msg_peg_nums = ""
    msg_move_types = ""

    # Go through every tuple in peg_list, convert to string and add to msg strings
    for ind,elm in enumerate(peg_list):
        if ind == len(peg_list) -1:
            msg_peg_nums += str(elm[0])
            msg_move_types += str(elm[1])
        else:
            msg_peg_nums += str(elm[0]) + ","
            msg_move_types += str(elm[1]) + ","

    # Combine peg_num and move_type msg strings
    msg_send = msg_peg_nums + ";" + msg_move_types
    print(msg_send)

    # Send message to Arduino
    msg_send = msg_send.encode() #'utf-8'
    serial_port.write(msg_send)

    # While no response is received, keep checking for response
    while no_response:
        time.sleep(1)
        response = serial_port.readline().decode()
        # If received response then print and end function
        if response is not None and len(response) > 0:
            print("Message from arduino: ", response)
            no_response = False
            response = None

# peg_list_test = [(1, 1), (40, 0), (20, 1), (0, 0)]
# peg_list_test = [(1,0), (43, 0), (1, 0), (2, 0), (43, 0), (4, 0), (40, 0), (0, 0)]
# peg_list_test = [(85,1), (84,1), (83, 1)]
# peg_list_test = [(40,0), (37, 1), (46, 0)]
# peg_list_card2 = [(25, 0), (20, 0)]
peg_list_card2 = [(38, 1), (28, 1), (42, 1),(66,0),(20,1),(40,0),(52,1),(37,1),(32,1),(7,0),(84,1),(0,1)]
# peg_list_card2 = [(14,0),(7,0),(84,0),(0,0),(67,0),(62,0),(61,0),(74,0),(7,0),(24,0),(0,0),(72,0),(0,0),(40,0),(22,0),(84,0),(0,0),(14,0),(7,0),(84,0),(0,0),(67,0),(62,0),(0,0), (72,0),(0,0),(40,0),(22,0),(84,0),(0,0),(14,0),(7,0),(84,0),(0,0),(67,0),(62,0), (72,0),(0,0),(40,0),(22,0),(84,0),(0,0),(14,0),(7,0),(84,0),(0,0),(67,0),(62,0), (0,0)]
peg_list_card = [(1, 1), (2, 0), (3, 1), (3, 0), (4, 1), (4, 0), (6, 1), (5, 0), (7, 1), (6, 0), (9, 1), (7, 0), (10, 1), (8, 0), (12, 1), (9, 0), (13, 1), (10, 0), (15, 1), (11, 0), (16, 1), (12, 0), (18, 1), (13, 0), (19, 1), (14, 0), (21, 1), (15, 0), (22, 1), (16, 0), (24, 1), (17, 0), (25, 1), (18, 0), (27, 1), (19, 0), (28, 1), (20, 0), (30, 1), (21, 0), (31, 1), (22, 0), (33, 1), (23, 0), (34, 1), (24, 0), (36, 1), (25, 0), (37, 1), (26, 0), (39, 1), (27, 0), (40, 1), (28, 0), (42, 1), (29, 0), (43, 1), (30, 0), (45, 1), (31, 0), (46, 1), (32, 0), (48, 1), (33, 0), (49, 1), (34, 0), (51, 1), (35, 0), (52, 1), (36, 0), (54, 1), (37, 0), (55, 1), (38, 0), (57, 1), (39, 0), (58, 1), (40, 0), (60, 1), (41, 0), (61, 1), (42, 0), (63, 1), (43, 0), (64, 1), (44, 0), (66, 1), (45, 0), (67, 1), (46, 0), (69, 1), (47, 0), (70, 1), (48, 0), (72, 1), (49, 0), (73, 1), (50, 0), (75, 1), (51, 0), (76, 1), (52, 0), (78, 1), (53, 0), (79, 1), (54, 0), (81, 1), (55, 0), (82, 1), (56, 0), (84,1), (57, 0), (85, 1), (58, 0), (87, 1), (59, 0), (88, 1), (60, 0), (90, 1), (61, 0), (91, 1), (62, 0), (93, 1), (63, 0), (94, 1), (64, 0), (0, 1), (65, 0), (1, 1), (66, 0), (3, 1), (67, 0), (4, 1), (68, 0), (6, 1), (69, 0), (7, 1), (70, 0), (9, 1), (71, 0), (10, 1), (72, 0), (12, 1), (73, 0), (13, 1), (74, 0), (15, 1), (75, 0), (16, 1), (76, 0), (18, 1), (77, 0), (19, 1), (78, 0), (21, 1), (79, 0), (22, 1), (80, 0), (24, 1), (81, 0), (25, 1), (82, 0), (27, 1), (83, 0), (28, 1), (84, 0), (30, 1), (85, 0), (31, 1), (86, 0), (33, 1), (87, 0), (34, 1), (88, 0), (36, 1), (89, 0), (37, 1), (90, 0), (39, 1), (91, 0), (40, 1), (92, 0), (42, 1), (93, 0), (43, 1), (94, 0), (45, 1), (95, 0), (46, 1), (96, 0), (0, 1), (1, 0)]
# peg_list_demo = [(1,0), (73, 1), (74, 0), (3,1), (4,0), (75,1), (76,0), (5, 1)]
peg_list_demo = [(73,1)]

# Variables needed for serial port communication
baudRate = 9600
arduinoComPort = "COM6"

# Set up serial port and send initialization message
print("Sending Initialization Message")
serial_port = serial.Serial(arduinoComPort, baudRate, timeout=1)
msg_send = "Initializing"
msg_send = msg_send.encode()
serial_port.write(msg_send)
time.sleep(1)

# Break up peg_list into sublists of <= 20 elements
peg_list = peg_list_card2
num_msgs = int(len(peg_list)/20)
print("Number of peg lists", num_msgs)
print("Length of peg list", len(peg_list))
index = 0
while num_msgs > 0:
    send_list_and_receive_response(peg_list[index:index+20], serial_port)
    index = index + 20
    num_msgs = num_msgs - 1
# Don't forget to send the leftover tuples
if index < len(peg_list):
    send_list_and_receive_response(peg_list[index:], serial_port)

# Send "Finished message"
print("Sending Finished Message")
msg_send = "Finished"
msg_send = msg_send.encode()
serial_port.write(msg_send)

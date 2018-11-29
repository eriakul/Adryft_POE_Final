from src.simulation import *
from src.compute_directions import *
import sys
import time

def get_next_peg(peg_list):
    if not peg_list:
        return False, 0
    temp_peg = peg_list.pop(0)
    return True, temp_peg[0], temp_peg[1]

peg_list = [20, 37]
#peg_list = [20, 40, 30, 10, 0]
#peg_list = [1, 3, 6, 10, 15, 21, 28, 36, 45, 7, 18, 30, 43, 9, 24, 40, 9, 27, 46, 18, 39, 13, 36, 12, 37, 15, 42, 22, 3, 33, 16, 48, 33, 19, 6, 42, 31, 21, 12, 4, 45, 39, 34, 30, 27, 25, 24, 24, 25]
peg_list_test = [(1, 1), (42, 0), (1, 1), (2,0)]
peg_list_card = [(1, 1), (2, 0), (3, 1), (3, 0), (4, 1), (4, 0), (6, 1), (5, 0), (7, 1), (6, 0), (9, 1), (7, 0), (10, 1), (8, 0), (12, 1), (9, 0), (13, 1), (10, 0), (15, 1), (11, 0), (16, 1), (12, 0), (18, 1), (13, 0), (19, 1), (14, 0), (21, 1), (15, 0), (22, 1), (16, 0), (24, 1), (17, 0), (25, 1), (18, 0), (27, 1), (19, 0), (28, 1), (20, 0), (30, 1), (21, 0), (31, 1), (22, 0), (33, 1), (23, 0), (34, 1), (24, 0), (36, 1), (25, 0), (37, 1), (26, 0), (39, 1), (27, 0), (40, 1), (28, 0), (42, 1), (29, 0), (43, 1), (30, 0), (45, 1), (31, 0), (46, 1), (32, 0), (0, 1), (33, 0), (1, 1), (34, 0), (3, 1), (35, 0), (4, 1), (36, 0), (6, 1), (37, 0), (7, 1), (38, 0), (9, 1), (39, 0), (10, 1), (40, 0), (12, 1), (41, 0), (13, 1), (42, 0), (15, 1), (43, 0), (16, 1), (44, 0), (18, 1), (45, 0), (19, 1), (46, 0), (21, 1), (47, 0), (22, 1), (48, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 1), (3, 0), (4, 1), (4, 0), (6, 1), (5, 0), (7, 1), (6, 0), (9, 1), (7, 0), (10, 1), (8, 0), (12, 1), (9, 0), (13, 1), (10, 0), (15, 1), (11, 0), (16, 1), (12, 0), (18, 1), (13, 0), (19, 1), (14, 0), (21, 1), (15, 0), (22, 1), (16, 0), (24, 1), (17, 0), (25, 1), (18, 0), (27, 1), (19, 0), (28, 1), (20, 0), (30, 1), (21, 0), (31, 1), (22, 0), (33, 1), (23, 0), (34, 1), (24, 0), (36, 1), (25, 0), (37, 1), (26, 0), (39, 1), (27, 0), (40, 1), (28, 0), (42, 1), (29, 0), (43, 1), (30, 0), (45, 1), (31, 0), (46, 1), (32, 0), (0, 1), (33, 0), (1, 1), (34, 0), (3, 1), (35, 0), (4, 1), (36, 0), (6, 1), (37, 0), (7, 1), (38, 0), (9, 1), (39, 0), (10, 1), (40, 0), (12, 1), (41, 0), (13, 1), (42, 0), (15, 1), (43, 0), (16, 1), (44, 0), (18, 1), (45, 0), (19, 1), (46, 0), (21, 1), (47, 0), (22, 1), (48, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 1), (3, 0), (4, 1), (4, 0), (6, 1), (5, 0)]


peg_num = 48
string_thickness = 1
max_string = 2000
real_radius = 1
max_overlap = 2
window_size = [1200, 800]
baudRate = 9600

arduinoComPort = "COM6"
pygame.init()

stringomatic = System(window_size, peg_num = peg_num, string_thickness = string_thickness)

half_step = 180/peg_num
current_location = [0,0] #r, theta (degrees)
peg_locations = list([360/peg_num* i for i in range(peg_num)])


print("Sending Initialization Message")
# Set up serial port and send initialization message
serial_port = serial.Serial(arduinoComPort, baudRate, timeout=1)
msg_send = "Initializing"
msg_send = msg_send.encode() #'utf-8'
serial_port.write(msg_send)
time.sleep(1)

print("Sending Wrap Commands")
#Send wrap commands in form "r;theta;r;r;theta;r;"
wrap_commands = create_wrap_commands(half_step, real_radius)
wrap_commands = "W" + wrap_commands
wrap_commands = wrap_commands.encode() #'utf-8'
serial_port.write(wrap_commands)
no_response = True
while no_response:
    time.sleep(1)
    response = serial_port.readline().decode()
    if response is not None and len(response) > 0:
        print("Message from arduino: ", response)
        no_response = False

print("Wrap Commands Sent")

check = True #checks if string art is complete
done = False #checks if pygame window should be open
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.image.save(stringomatic.screen, "hardcoded_result.jpeg")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE:
                check = not check

    if check:
        check1, next_peg1, move_type1 = get_next_peg(peg_list_test)
        check2, next_peg2, move_type2 = get_next_peg(peg_list_test)
        print("Next peg indexs: {} and {}".format(next_peg1, next_peg2))
        if check2:
            stringomatic.draw_line_to(next_peg1)
            stringomatic.update_window()
            peg_loc1 = peg_locations[next_peg1]
            peg_loc2 = peg_locations[next_peg2]
            print("Projected peg location: {}".format(peg_loc2))
            current_location, commands = loop_around_peg(current_location, peg_loc1, half_step, real_radius, peg_loc2)
            print("Projected commands: {}".format(commands))
            print("Projected final location: {}".format(current_location))
            for command in commands:
                print("Sent: {}".format(command))
                send_command_and_receive_response(command, serial_port)




    else:
        sleep(.1)

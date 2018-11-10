
import serial
import numpy as np
import re
import time

def convert_angle_to_within_range(angle):
    angle = angle%360
    if angle < 0:
        angle += 360
    return angle

def update_current_location(current_location, command):
    r_current = current_location[0]
    theta_current = current_location[1]
    dr = command[0]
    dtheta = command[1]
    return [r_current + dr, convert_angle_to_within_range(theta_current + dtheta)]

def loop_around_peg(current_location, peg_location, half_step, r):
        """
        Receives: current_location, peg_location
        Returns: new current_location and list of commands
        """
        commands = []

        target_location_B = [peg_location - half_step, peg_location - half_step - 360]
        loc_B0 = convert_angle_to_within_range(-1*current_location[1])
        loc_B180 = convert_angle_to_within_range(loc_B0+180)

        if min([abs(loc - loc_B0) for loc in target_location_B]) <= min([abs(loc - loc_B180) for loc in target_location_B]):
            direction = "North"
            tL = min(target_location_B, key = lambda loc: abs(loc - loc_B0))
            dtheta = tL-loc_B0
            dr_in = r*.9 - current_location[0]
            dr_out = r*.2
            dr_back = -1*dr_out

        else:
            direction = "South"
            tL = min(target_location_B, key = lambda loc: abs(loc - loc_B180))
            dtheta = tL - loc_B180
            dr_in = r*-.9 - current_location[-0]
            dr_out = r*-.2
            dr_back = -1*dr_out


        command = [dr_in, dtheta]
        commands.append(command)
        current_location = update_current_location(current_location, command)

        command = [dr_out, 0]
        commands.append(command)
        current_location = update_current_location(current_location, command)

        command = [0, 2*half_step]
        commands.append(command)
        current_location = update_current_location(current_location, command)

        command = [dr_back, 0]
        commands.append(command)
        current_location = update_current_location(current_location, command)

        return current_location, commands



def process_peg_list(peg_num, peg_list, real_board_radius):
    """
    Receives: peg_list
    Returns: d_theta and d_r per time step
    """
    half_step = 180/peg_num
    current_location = [0,0] #r, theta (degrees)
    peg_loc = list([360/peg_num* i for i in range(peg_num)])
    command_list = []

    for i in peg_list[1:]:
        peg_location = peg_loc[i]
        current_location, commands = loop_around_peg(current_location, peg_location, half_step, real_board_radius)
        command_list = command_list + commands
        print("Commands: {}\nCurrent Location: {}".format(commands, current_location))
    return command_list


def send_command_and_receive_response(command, serial_port):
    # Send command to Arduino
    no_response = True
    response = None
    serial_port.flush()
    radius = str(command[0])
    theta = str(command[1])
    msg_send = radius + "," + theta
    msg_send = msg_send.encode() #'utf-8'
    # Send message in the form of radius,theta
    serial_port.write(msg_send)
    print("Python value sent: ", msg_send)
    # While no response is received, keep checking for response
    while no_response:
        time.sleep(1)
        response = serial_port.readline().decode()
        if response is not None and len(response) > 0:
            print("Message from arduino: ", response)
            no_response = False
            response = None

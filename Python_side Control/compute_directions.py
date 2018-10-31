peg_list = [0, 26, 77, 25, 75, 24, 74, 23, 67, 22, 68, 18, 69, 17, 66, 16, 70, 20, 71, 21, 72, 19, 73, 34, 85, 12, 64, 13, 65, 15, 54, 14, 53, 3, 76, 25, 77, 24, 75, 23, 67, 22, 68, 18, 69, 17, 66, 16, 70, 20, 71, 21, 72, 32, 73, 19, 74, 35, 87, 26, 78, 39, 0, 28, 79, 27, 86, 13, 65, 15, 54, 14, 64, 12, 67, 23, 68, 22, 69, 17, 66, 16, 70, 20, 71, 21, 72, 18, 73, 24, 77, 25, 81, 42, 3, 76, 37, 56, 5, 65, 13, 51, 11, 64, 14, 67, 23, 68, 22, 69, 17, 66, 16, 55, 15, 70, 20, 71, 21, 72, 18, 75, 24, 77, 25, 82, 9, 48, 88, 26, 78, 19, 74, 1, 27, 84, 11, 65, 13, 64, 12, 67, 22, 68, 23, 69, 17, 66, 15, 71, 20, 70, 14, 73, 21, 72, 16, 55, 36, 75, 18, 57, 7, 78, 24, 79, 6, 45, 85, 25, 76, 3, 64, 12, 67, 22, 69, 23, 68, 17, 56, 37, 77, 20, 66, 15, 65, 13, 70, 19, 74, 14, 75, 18, 57, 7, 78, 24, 80, 9, 61, 10, 62, 11, 64, 12, 67, 22, 69, 23, 68, 21, 71, 31, 72, 16, 66, 15, 65, 8, 47, 86, 13, 70, 19, 59, 20, 77, 25, 76, 24, 80, 9, 82, 43, 81, 29, 5, 64, 14, 67, 23, 69, 22, 74, 21, 68, 17, 56, 37, 54, 15, 66, 13, 70, 19, 78, 7, 65, 11, 84, 24, 80, 20, 2, 75, 18, 57, 38, 77, 39, 0, 72, 16, 67, 12, 51, 1, 23, 69, 21, 68, 17, 56, 37, 54, 15, 66, 13, 70, 19, 59, 8, 64, 14, 85, 24, 80, 20, 81, 18, 57, 38, 89, 16, 67, 11, 65, 10, 62, 12, 51, 1, 75, 23, 79, 21, 69, 15, 71, 31, 70, 13, 66, 7, 78, 26, 83, 9, 48, 88, 18, 68, 17, 56, 37, 54, 35, 52, 34, 74, 19, 67, 16, 55, 36, 76, 24, 80, 23, 75, 22, 70, 12, 51, 11, 66, 13, 69, 21, 79, 6, 45, 64, 14, 53, 3, 42, 2, 73, 17, 68, 18, 57, 38, 89, 16, 67, 19, 78, 7, 65, 15, 54, 35, 75, 22, 70, 23, 80, 28, 84, 11, 66, 10, 62, 9, 83, 20, 60, 21, 79, 6, 45, 85, 12, 51, 13, 52, 34, 53, 14, 67, 16, 55, 36, 74, 17, 56, 39, 58, 18, 68, 11, 70, 23, 80, 8, 64, 9, 83, 20, 60, 19, 78, 26, 84, 21, 79, 6, 45, 85, 12, 51, 1, 75, 22, 77, 4, 65, 7, 66, 10, 68, 16, 55, 36, 53, 34, 52, 13, 87, 69, 29, 70, 23, 76, 3, 64, 8, 80, 17, 67, 21, 79, 6, 45, 26, 78, 19, 60, 20, 77, 22, 75, 14, 85, 11, 71, 15, 72, 0, 18, 1, 51, 13, 52, 12, 70, 23, 76, 16, 68, 10, 62, 86, 24, 73, 2, 64, 8, 80, 17, 67, 21, 69, 29, 48, 9, 83, 20, 60, 19, 79, 40, 78, 22, 77, 4, 65, 46, 6, 28, 47, 66, 7, 81, 24, 73, 0, 16, 68, 10, 71, 15, 72, 11, 85, 21, 67, 17, 80, 8, 64, 9, 83, 20, 60, 19, 70, 23, 42, 61, 5, 65, 4, 77, 14, 54, 35, 55, 36, 53, 34, 16, 68, 10, 62, 12, 63, 7, 66, 13, 52, 2, 64, 9, 48, 67, 17, 80, 8, 82, 24, 73, 0, 29, 69, 21, 87, 19, 79, 26, 45, 85, 11, 72, 15, 55, 35, 54, 14, 66, 7, 65, 4, 77, 27, 89, 64, 9, 68, 16, 76, 23, 42, 61, 20, 67, 17, 80, 22, 70, 12, 63, 44, 25, 72, 15, 55, 35, 54, 14, 53, 34, 52, 13, 69, 29, 48, 66, 5, 68, 9, 84, 23, 42, 61, 20, 67, 19, 79, 16, 81, 22, 70, 12, 63, 7, 65, 4, 77, 27, 88, 17, 74, 0, 39, 58, 18, 75, 13, 69, 29, 48, 9, 68, 21, 60, 80, 26, 45, 85, 11, 67, 19, 66, 12, 70, 22, 81, 16, 56, 36, 53, 34, 52, 33, 72, 15, 55, 17, 74, 0, 39, 58, 18, 2, 73, 24, 71, 10, 68, 9, 84, 20, 67, 19, 66, 12, 69, 85, 11, 70, 29, 48, 88, 13, 51, 32, 72, 25, 44, 62, 86, 22, 81, 16, 56, 39, 58, 18, 73, 2, 53, 14, 77, 27, 46, 6, 28, 47, 8, 65, 9, 68, 21, 67, 20, 84, 19, 66, 5, 70, 29, 48, 88, 72, 11, 51, 13, 63, 7, 81, 16, 56, 39, 58, 18, 69, 12, 52, 33, 73, 2, 53, 71, 24, 43, 4, 68, 20, 67, 14, 77, 27, 46, 6, 28, 47, 8, 65, 9, 84, 19, 66, 5, 70, 29, 82, 10, 72, 25, 44, 64, 13, 88, 48, 87, 15, 55, 17, 74, 24, 71, 31, 50, 12, 52, 33, 14, 67, 21, 60, 80, 41, 79, 5, 66, 19, 69, 85, 68, 20, 61, 42, 23, 76, 3, 63, 7, 81, 16, 2, 53, 71, 24, 43, 4, 64, 13, 88, 72, 10, 67, 15, 87, 37, 54, 12, 52, 33, 84, 9, 74, 19, 69, 85, 68, 20, 61, 42, 23, 76, 21, 60, 80, 62, 86, 29, 70, 11, 51, 1, 71, 24, 43, 4, 63, 8, 47, 28, 6, 46, 27, 77, 14, 81, 26, 45, 5, 66, 12, 52, 33, 50, 68, 20, 61, 19, 69, 85, 9, 30, 49, 11, 51, 67, 15, 71, 31, 70, 17, 55, 35, 56, 16, 76, 21, 60, 79, 29, 5, 22, 41, 80, 62, 86, 20, 68, 4, 43, 24, 82, 8, 65, 2, 52, 14, 81, 7, 83, 61, 6, 67, 15, 73, 0, 74, 9, 30, 71, 23, 72, 10, 50, 31, 70, 11, 49, 68, 85, 69, 19, 79, 5, 29, 4, 43, 24, 89]

peg_list = [0,1,2,3,1]

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
            dtheta = loc_B0 - tL
            dr_in = r*.9 - current_location[0]
            dr_out = r*.2
            dr_back = -1*dr_out

        else:
            direction = "South"
            tL = min(target_location_B, key = lambda loc: abs(loc - loc_B180))
            dtheta = loc_B180 - tL
            dr_in = r*-.9 - current_location[-0]
            dr_out = r*-.2
            dr_back = -1*dr_out


        command = [dr_in, dtheta]
        commands.append(command)
        current_location = update_current_location(current_location, command)

        command = [dr_out, 0]
        commands.append(command)
        current_location = update_current_location(current_location, command)

        command = [0, -2*half_step]
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

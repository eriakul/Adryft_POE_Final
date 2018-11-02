#C:\Users\elu\Documents\_Code\Adryft_POE_Final\Python_side Control

from src.simulation import *
from src.compute_directions import *
import sys

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == 'custom':
            file_name = input("File Name: ")
            peg_num = input("Number of Pegs: ")
            string_thickness = input("string Thickness: ")
            max_string = input("Spool Length: ")
            real_radius = input("Board Radius: ")
            max_overlap = input("Max Overlap: ")
            baudRate = 9600
            window_size = [1200, 800]
        else:
            print("Unidentified command.")

    else:

        ##### EDIT SETTINGS HERE #######

        file_name = "pokeball.jpeg"
        peg_num = 45
        string_thickness = 1
        max_string = 2000
        real_radius = 1
        max_overlap = 2
        window_size = [1200, 800]
        baudRate = 9600

    arduinoComPort = "COM7"
    pygame.init()

    stringomatic = System(window_size, peg_num = peg_num, string_thickness = string_thickness)
    image = ImageProcessor(file_name, peg_num = peg_num, string_thickness = string_thickness,
                            real_radius = real_radius, max_overlap = max_overlap)
    stringomatic.add_image_information(image)

    half_step = 180/peg_num
    current_location = [0,0] #r, theta (degrees)
    peg_locations = list([360/peg_num* i for i in range(peg_num)])

    serial_port = serial.Serial(arduinoComPort, baudRate, timeout=1)

    check = True #checks if string art is complete
    done = False #checks if pygame window should be open
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                file_name = file_name.split(".")[0] + "_{}_{}".format(peg_num, real_radius).replace(".", "")
                pygame.image.save(stringomatic.screen, file_name +"_result")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    check = not check

        if image.total_string_cost < max_string and check:
            check, next_peg = stringomatic.draw_mesh_live(image)
            if check:
                peg_loc = peg_locations[next_peg]
                current_location, commands = loop_around_peg(current_location, peg_loc, half_step, real_radius)
                for command in commands:
                    send_command_and_receive_response(command, serial_port)




        else:
            sleep(.1)

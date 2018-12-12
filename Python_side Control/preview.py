import pygame
from math import floor, pi, cos, sin, hypot
from time import sleep
from operator import itemgetter
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from itertools import combinations
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, show
#pip install Pillow==3.1.2
import os



class System:

    """ System is a class that processes the live Pygame display of the string art simulator."""

    def __init__(self, window_size, peg_num = 96, string_thickness = 1, peg_size = 5):
        """Initializes Pygame window with given settings."""

        self.window_size = window_size
        self.font = pygame.font.SysFont('tlwgtypewriter', 30)
        self.text_position = [window_size[0]//10, window_size[1]//10]

        self.peg_num = peg_num
        self.screen_properties = dict(
            board_color = pygame.Color(255, 255, 255, 255),
            board_radius = floor(window_size[1]/2*.9),
            center = [window_size[0]//2, window_size[1]//2],
            pegs = [],
            peg_size = peg_size,
            peg_color = pygame.Color(100, 100, 100, 255),
            peg_highlight = pygame.Color(100, 255, 255, 255),
            string_color = pygame.Color(0, 0, 0, 255),
            string_thickness = string_thickness
            )

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("String Art Simulation")
        pygame.draw.circle(self.screen,
                            self.screen_properties["board_color"],
                            self.screen_properties["center"],
                            self.screen_properties["board_radius"])
        pygame.display.flip()
        self.create_pegs()
        self.refresh_pegs()



    def update_window(self):
        pygame.display.flip()


    def create_pegs(self):
        angle_steps = 2*pi/self.peg_num
        peg_locations = []
        radius = self.screen_properties["board_radius"]
        center_x = self.screen_properties["center"][0]
        center_y = self.screen_properties["center"][1]
        for i in range(self.peg_num):
            theta = 3/2*pi +i*angle_steps
            x_delta = radius*cos(theta)
            y_delta = radius*sin(theta)
            location = [floor(center_x + x_delta), floor(center_y + y_delta)]
            peg_locations.append(location)

        self.screen_properties["pegs"] = peg_locations
        self.current_peg = self.screen_properties["pegs"][0]

    def refresh_pegs(self):
        for location in self.screen_properties["pegs"]:
            pygame.draw.circle(self.screen,
                                self.screen_properties["peg_color"],
                                location,
                                self.screen_properties["peg_size"])
        #highlight current peg
        pygame.draw.circle(self.screen,
                            self.screen_properties["peg_highlight"],
                            self.current_peg,
                            self.screen_properties["peg_size"])

    def process_click(self):
        x, y = event.pos
        closest_peg = min(self.screen_properties["pegs"],
        key = lambda pos: hypot(pos[0]-x, pos[1]-y))

        pygame.draw.line(self.screen, self.screen_properties["string_color"],
                        self.current_peg, closest_peg, self.screen_properties["string_thickness"])

        self.current_peg = closest_peg
        self.refresh_pegs()
        self.update_window()

    def draw_line_to(self, peg_index):
        last_peg = self.current_peg
        current_peg = self.screen_properties["pegs"][peg_index]
        # pygame.draw.line(self.screen, self.screen_properties["string_color"],
        #                 last_peg, current_peg, self.screen_properties["string_thickness"])
        pygame.draw.aaline(self.screen, self.screen_properties["string_color"],
                        last_peg, current_peg, True)

        self.current_peg = current_peg
        self.refresh_pegs()

    def update_string_used(self, string_used):
        string_used = "{} ft".format(round(string_used, 1))
        new_display = self.font.render(string_used, False, (255, 255, 255, 255), (0,0,0,0))
        self.screen.blit(new_display, self.text_position)

    def draw_mesh(self, peg_list):
        """Draws a mesh from peg to peg.
        peg_list -- list of consecutive pegs that need to be connected, number in list refers to peg number
        """
        current_index = 0
        #Iterate through peg_list and draw lines from peg to peg
        for i in range(0, len(peg_list) - 1):
            if peg_list[i][1] == 0:
                from_peg = peg_list[i-1][0]-1 #starting point of line
                to_peg = peg_list[i][0]-1 #end point of line

                pygame.draw.line(self.screen, self.screen_properties["string_color"],
                            self.screen_properties["pegs"][from_peg], self.screen_properties["pegs"][to_peg], self.screen_properties["string_thickness"])


        self.current_peg = self.screen_properties["pegs"][peg_list[-1][0]] #last peg in list becomes the peg to start for process_click()
        self.refresh_pegs()
        self.update_window()

    def draw_mesh_live(self, ImageProcessor):
        next_peg = ImageProcessor.find_next_peg()

        if next_peg == self.current_peg:
            return False, 0

        self.draw_line_to(next_peg)

        self.update_string_used(ImageProcessor.total_string_cost)

        self.update_window()

        ImageProcessor.mean_squared_error()

        return True, next_peg

    def add_to_histogram(self, peg_1, peg_2):
        self.histogram[frozenset([peg_1, peg_2])] = self.histogram.get(frozenset([peg_1, peg_2]), 0) + 1
    def add_image_information(self, ImageProcessor):
        data = "{} pegs : {} ft radius : {} max-overlap".format(self.peg_num, ImageProcessor.real_radius, ImageProcessor.max_overlap)
        new_display = self.font.render(data, False, (255, 255, 255, 255), (0,0,0,0))
        self.screen.blit(new_display, [int(.1/10*self.window_size[0]), int(0/10*self.window_size[1])])




if __name__ == "__main__":

    pygame.init()

    file_name = "pokeball.jpeg"

    peg_num = 96
    string_thickness = 1
    max_string = 3000
    real_radius = 1
    max_overlap = 2

    window_size = [1200, 800]

    from cardioid import peg_list

    stringomatic = System(window_size, peg_num = peg_num, string_thickness = string_thickness)

    stringomatic.draw_mesh(peg_list)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True


            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     stringomatic.process_click()

        # if image.total_string_cost < max_string and check:
        #     check = stringomatic.draw_mesh_live(image)
        else:
            sleep(.1)

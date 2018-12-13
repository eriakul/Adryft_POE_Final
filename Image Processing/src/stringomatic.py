import pygame
from math import floor, pi, cos, sin, hypot
from time import sleep
from operator import itemgetter
import numpy
import cv2

class System:
    def __init__(self, window_size, peg_num = 36, string_thickness = 1, peg_size = 5):
        self.peg_num = peg_num

        self.screen_properties = dict(
            board_color = pygame.Color(255, 255, 255, 255),
            board_radius = floor(window_size[1]/2*.9),
            center = [floor(window_size[0]/2), floor(window_size[1]/2)],
            pegs = [],
            peg_size = peg_size,
            peg_color = pygame.Color(100, 100, 100, 255),
            peg_highlight = pygame.Color(100, 255, 255, 255),
            string_color = pygame.Color(0, 0, 0, 255),
            string_thickness = string_thickness
            )

        self.window_name= "StringOmatic"
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, 1)
        #Draw circle CV
        cv2.circle(self.window_name,
                    self.screen_properties["center"],
                    self.screen_properties["board_radius"],
                    self.screen_properties["board_color"])

        self.create_pegs()
        self.current_peg = self.screen_properties["pegs"][0]
        self.refresh_pegs()



    def update_window(self):
        pass

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

    def refresh_pegs(self):
        for location in self.screen_properties["pegs"]:
            cv2.circle(self.window_name,
                        location,
                        self.screen_properties["peg_size"],
                        self.screen_properties["peg_color"])
        cv2.circle(self.window_name,
                    location,
                    self.screen_properties["peg_size"],
                    self.screen_properties["peg_highlight"])
        cv2.imshow(self.window_name)
        #highlight current peg

    def process_click(self):
        x, y = event.pos
        last_peg = self.current_peg
        closest_peg = min(self.screen_properties["pegs"],
        key = lambda pos: hypot(pos[0]-x, pos[1]-y))

        pygame.draw.line(self.screen, self.screen_properties["string_color"],
                        last_peg, closest_peg, self.screen_properties["string_thickness"])

        self.current_peg = closest_peg
        self.refresh_pegs()
        imshow(self.window_name)


if __name__ == "__main__":

    window_size = [1000, 500]

    stringomatic = System(window_size, peg_num = 36)
    done = False
    cv2.setMouseCallback('The Window Name', turret.mouse_callback)


    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break
        sleep(.05)

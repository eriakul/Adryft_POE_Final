import pygame
from math import floor, pi, cos, sin, hypot
from time import sleep
from operator import itemgetter
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from itertools import combinations
#pip install Pillow==3.1.2
import os


class System:
    def __init__(self, window_size, peg_num = 36, string_thickness = 1, peg_size = 5):
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
        pygame.display.flip()
    def process_click(self):
        x, y = event.pos
        last_peg = self.current_peg
        closest_peg = min(self.screen_properties["pegs"],
        key = lambda pos: hypot(pos[0]-x, pos[1]-y))

        pygame.draw.line(self.screen, self.screen_properties["string_color"],
                        last_peg, closest_peg, self.screen_properties["string_thickness"])

        self.current_peg = closest_peg
        self.refresh_pegs()

    def draw_image(self, peg_list):
        """Draws a mesh from peg to peg.
        peg_list -- list of consecutive pegs that need to be connected, number in list refers to peg number
        """
        #Iterate through peg_list and draw lines from peg to peg
        for i in range(len(peg_list) - 1):
            from_peg = peg_list[i] #starting point of line
            to_peg = peg_list[i + 1] #end point of line

            pygame.draw.line(self.screen, self.screen_properties["string_color"],
                            self.screen_properties["pegs"][from_peg], self.screen_properties["pegs"][to_peg], self.screen_properties["string_thickness"])


        self.current_peg = self.screen_properties["pegs"][peg_list[-1]] #last peg in list becomes the peg to start for process_click()
        self.refresh_pegs()

class ImageProcessor:
    def __init__(self, file_name, peg_num = 36, string_thickness = 1, max_lines = 1000):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.peg_num = peg_num
        self.max_lines = max_lines
        self.string_thickness = string_thickness

        self.image = Image.open(dir_path+"/"+file_name)
        self.image_size = self.image.size
        self.diameter = floor(min(self.image_size))

        self.peg_list = []
        self.pegs = []
        self.previous_pegs = list([0 for i in range(peg_num//3)])
        self.current_index = 0


        self.crop_image_to_square()

        self.turn_image_grayscale()
        self.invert_image()
        self.crop_circle()
        self.create_pegs()
        # self.show_pegs()

        self.np_image = np.asarray(self.image.getdata(),dtype=np.float64).reshape((self.image.size[1], self.image.size[0]))

        self.compute_lines()


        # self.image_center = [floor(self.image_size[0]/2), floor(self.image_size[1]/2)]
        # print("Image Center: ", self.image_center)

    def crop_image_to_square(self):
        crop_rectangle =((self.image_size[0]-self.diameter)//2,
                        (self.image_size[1]-self.diameter)//2,
                        (self.image_size[0]+self.diameter)//2,
                        (self.image_size[1]+self.diameter)//2)
        self.image = self.image.crop(crop_rectangle)
        self.image_size = self.image.size
        self.image_center = [self.image.size[0]//2, self.image.size[1]//2]


    def turn_image_grayscale(self):
        self.image = self.image.convert('L')

    def invert_image(self):
        self.image = ImageOps.invert(self.image)

    def crop_circle(self):
        black_image = Image.new('L', self.image_size, 0)
        mask = Image.new('L', self.image_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + self.image_size, fill=255)
        self.image = Image.composite(self.image, black_image, mask)

    def create_pegs(self):
        angle_steps = 2*pi/self.peg_num
        peg_locations = []
        radius = self.diameter//2
        center_x = self.image_center[0]
        center_y = self.image_center[1]
        for i in range(self.peg_num):
            theta = 3/2*pi +i*angle_steps
            x_delta = radius*cos(theta)
            y_delta = radius*sin(theta)
            location = (floor(center_x + x_delta), floor(center_y + y_delta))
            peg_locations.append(location)
        self.pegs = peg_locations

    def show_pegs(self):
        draw = ImageDraw.Draw(self.image)
        draw.point(self.pegs, fill=255)
        self.image.show()

    def compute_lines(self):

        peg_combinations = combinations(range(self.peg_num), 2)
        self.line_dict = {}

        for index_set in peg_combinations:
            peg_1 = self.pegs[index_set[0]]
            peg_2 = self.pegs[index_set[1]]
            length = int(np.hypot(peg_2[0] - peg_1[0], peg_2[1] - peg_1[1]))
            xs = np.linspace(peg_1[0]-2, peg_2[0]-2, length).tolist()
            ys = np.linspace(peg_1[1]-2, peg_2[1]-2, length).tolist()
            xs = list(map(int, xs))
            ys = list(map(int, ys))

            self.line_dict[frozenset([index_set[0], index_set[1]])] = [xs, ys]

    def compute_best_path(self):
        best_line = 0
        best_index = 0
        for index in range(self.peg_num):
            if index == self.current_index or index in self.previous_pegs:
                continue
            line = self.line_dict[frozenset([self.current_index, index])]
            line_fit = np.sum(self.np_image[line[1], line[0]])
            if line_fit > best_line:
                best_line = line_fit
                best_index = index

        return best_index

    def draw_line(self, peg_index):
        draw = ImageDraw.Draw(self.image)
        draw.line([self.pegs[self.current_index], self.pegs[peg_index]], fill=0, width = self.string_thickness)
        self.current_index = peg_index
        self.previous_pegs.append(peg_index)
        self.previous_pegs.pop(0)
        self.np_image = np.asarray(self.image.getdata(),dtype=np.float64).reshape((self.image.size[1], self.image.size[0]))

    def find_peg_list(self):
        line_num = 0
        while line_num < self.max_lines:
            line_num +=1
            best_peg = self.compute_best_path()
            self.draw_line(best_peg)
            self.peg_list.append(best_peg)

        return self.peg_list



if __name__ == "__main__":

    peg_num = 200
    string_thickness = 1
    max_lines = 1000

    window_size = [1200, 800]

    pygame.init()
    stringomatic = System(window_size, peg_num = peg_num, string_thickness = string_thickness)
    done = False
    logo = ImageProcessor("olinlogo.jpeg", peg_num = peg_num, string_thickness = string_thickness, max_lines = max_lines)
    peg_list = logo.find_peg_list()
    print(peg_list)
    stringomatic.draw_image(peg_list)



    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN :
                stringomatic.process_click()
        sleep(.05)

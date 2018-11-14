import pygame
from math import floor, pi, cos, sin, hypot
from time import sleep
from operator import itemgetter
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from itertools import combinations
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, show
import matplotlib.pyplot as plt
#pip install Pillow==3.1.2
import os


class System:

    """ System is a class that processes the live Pygame display of the string art simulator."""

    def __init__(self, window_size, peg_num = 36, string_thickness = 1, peg_size = 5):
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

    # def process_click(self):
    #     x, y = event.pos
    #     closest_peg = min(self.screen_properties["pegs"],
    #     key = lambda pos: hypot(pos[0]-x, pos[1]-y))
    #
    #     pygame.draw.line(self.screen, self.screen_properties["string_color"],
    #                     self.current_peg, closest_peg, self.screen_properties["string_thickness"])
    #
    #     self.current_peg = closest_peg
    #     self.refresh_pegs()
    #     self.update_window()

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
        #Iterate through peg_list and draw lines from peg to peg
        for i in range(len(peg_list) - 1):
            from_peg = peg_list[i] #starting point of line
            to_peg = peg_list[i + 1] #end point of line

            pygame.draw.line(self.screen, self.screen_properties["string_color"],
                            self.screen_properties["pegs"][from_peg], self.screen_properties["pegs"][to_peg], self.screen_properties["string_thickness"])


        self.current_peg = self.screen_properties["pegs"][peg_list[-1]] #last peg in list becomes the peg to start for process_click()
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
        data = "{} pegs : {} ft radius : {} max-overlap".format(self.peg_num, ImageProcessor.radius, ImageProcessor.max_overlap)
        new_display = self.font.render(data, False, (255, 255, 255, 255), (0,0,0,0))
        self.screen.blit(new_display, [int(.1/10*self.window_size[0]), int(0/10*self.window_size[1])])

class ImageProcessor:
    """This class takes an image and does the computing to determine where to draw the lines."""

    def __init__(self, file_name, num_pegs = 48, string_thickness = 0.01, max_length = 1500, radius = 11, debug = False):
        self.num_pegs = num_pegs                    #unitless
        self.max_length = max_length                #feet
        self.string_thickness = string_thickness    #inches
        self.radius = radius                        #inches
        self.total_string_cost = 0 #How much string we've used so far in feet
        self.debug = debug

        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Open image in grayscale
        self.image = Image.open(dir_path+"/"+file_name).convert('L')
        self.original_image_size = self.image.size
        self.crop_image_to_square()
        self.image_size = self.image.size
        self.crop_image_to_circle()
        print("Original Image Size: ", self.original_image_size)
        print("New Image Size: ", self.image_size)
        if debug:
            self.image.show()

        self.np_image = np.asmatrix(self.image.getdata(),dtype=np.float64).reshape(self.image_size[0], self.image_size[1])
        self.np_image = np.flipud(self.np_image)
        self.pegs = []
        self.create_pegs()
        self.pixel_x_coors, self.pixel_y_coors = self.create_pixel_to_inch_mesh()

        self.calc_all_paths()

    def crop_image_to_square(self):
        """ Transforms image into square the size of the smallest dimension """
        crop_size = floor(min(self.original_image_size))
        y = self.original_image_size[1]
        x = self.original_image_size[0]

        # Left, top, right, and bottom midpoints for the crop box
        crop_box = ((x - crop_size)//2,
                    (y - crop_size)//2,
                    (x + crop_size)//2,
                    (y + crop_size)//2)
        self.image = self.image.crop(crop_box)

    def crop_image_to_circle(self):
        """ Masks out circular outline of image to white """
        white_image = Image.new('L', self.image_size, 255)
        mask = Image.new('L', self.image_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + self.image_size, fill=255)
        self.image = Image.composite(self.image, white_image, mask)

    def create_pegs(self):
        """ Creates list of x-y points for each peg """
        dTheta = 2 * pi / self.num_pegs
        for peg_number in range(self.num_pegs):
            theta = peg_number * dTheta
            x = self.radius * cos(theta)
            y = self.radius * sin(theta)
            self.pegs.append((x, y))

    def create_pixel_to_inch_mesh(self):
        """ Create array of equal size to the image. Maps pixels to positions in physical space
        Returns: a 3D array =[image_width, image_height, xs;
                                image_width, image_height, ys]
        """
        xs = np.linspace(-self.radius, self.radius, self.image_size[0])
        ys = np.linspace(-self.radius, self.radius, self.image_size[1])
        return np.meshgrid(xs, ys)

    def calc_fitness(self, peg1, peg2):
        """ See how much a given line matches the image """
        peg1_pos = np.asmatrix([self.pegs[peg1][0], self.pegs[peg1][1]])
        peg2_pos = np.asmatrix([self.pegs[peg2][0], self.pegs[peg2][1]])

        string_vector = peg2_pos - peg1_pos
        v_hat = string_vector / np.linalg.norm(string_vector)
        n = self.pixel_x_coors.shape[1]
        pixel_points = np.concatenate((self.pixel_x_coors.reshape((1, n**2)),
                                self.pixel_y_coors.reshape((1, n**2))), axis=0)


        pixel_vectors = pixel_points - (peg1_pos.T * np.ones((1, n**2)))
        norms = np.linalg.norm(pixel_vectors - np.multiply(v_hat.T, np.dot(v_hat, pixel_vectors)), axis=0)
        norms = norms.reshape((n, n))

        valid_points = (norms < self.string_thickness*2)
        fitness = np.sum(self.np_image[valid_points])
        if self.debug or fitness == 0:
            for i, peg in enumerate(self.pegs):
                if i == peg1 or i == peg2:
                    plt.plot(peg[0], peg[1], 'ro')
                else:
                    plt.plot(peg[0], peg[1], 'ko')

            plt.contourf(self.pixel_x_coors, self.pixel_y_coors, norms, 20, cmap=plt.cm.viridis)
            cbar = plt.colorbar()
            plt.contour(self.pixel_x_coors, self.pixel_y_coors, self.np_image, 2)
            plt.axis("equal")
            plt.show()

            print("Fitness is: ", fitness)
        return fitness

    def calc_all_paths(self):
        """ Look at all possible paths and evaulate the "fitness" of each """
        self.line_list = []
        peg_combinations = combinations(range(self.num_pegs), 2)
        for combo in peg_combinations:
            peg1, peg2 = combo;
            fitness = self.calc_fitness(peg1, peg2)
            self.line_list.append((fitness, peg1, peg2))
            print(fitness)

    def calc_optimal_path(self):
        """ Pick the best paths in the right order to minimize string used """
        # Returns: list of tuples. Each tuple contains a peg combo
        # (from_peg, to_peg)
        pass

if __name__ == "__main__":
    test = ImageProcessor(file_name="nike.jpeg", debug=False)

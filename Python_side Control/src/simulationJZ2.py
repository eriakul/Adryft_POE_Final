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
from matplotlib import collections as mc

#pip install Pillow==3.1.2
import os
import pdb

class ImageProcessor:
    """This class takes an image and does the computing to determine where to draw the lines."""

    def __init__(self, file_name, num_pegs = 48, string_thickness = 0.05, max_length = 3000, radius = 11, max_image_size = 512, debug = False):
        self.num_pegs = num_pegs                    #unitless
        self.max_length = max_length * 12           #feet -> inches
        self.string_thickness = string_thickness    #inches
        self.radius = radius                        #inches
        self.total_string_cost = 0 #How much string we've used so far in feet
        self.debug = debug
        self.max_image_size = max_image_size
        self.file_name = file_name
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Open image in grayscale
        self.image = Image.open(dir_path+"/"+self.file_name).convert('L')
        self.original_image_size = self.image.size
        self.resize_image()
        self.crop_image_to_square()
        self.image_size = self.image.size
        self.crop_image_to_circle()
        print("Original Image Size: ", self.original_image_size)
        print("New Image Size: ", self.image_size)
        if self.debug:
            self.image.show()

        self.np_image = np.asmatrix(self.image.getdata(),dtype=np.float64).reshape(self.image_size[0], self.image_size[1])
        self.np_image = np.flipud(self.np_image)
        self.np_image = 255 - self.np_image
        if self.debug:
            plt.imshow(np.flipud(self.np_image))
            plt.show()
        self.pegs = []
        self.create_pegs()
        self.pixel_x_coors, self.pixel_y_coors = self.create_pixel_to_inch_mesh()

        # self.create_cardioid(2000, 0.5)
        # self.create_cardioid(2000, 1)
        self.create_cardioid(48, 1.5)
        # self.create_cardioid(2000, 2)
        # self.create_cardioid(2000, 4)
        self.calc_all_paths()
        self.calc_optimal_path(500 * 12)
        self.calc_optimal_path(1000*12)
        self.calc_optimal_path(1500 * 12)
        # self.calc_optimal_path(2500 * 12)
        # self.calc_optimal_path(3000 * 12)
        # self.calc_usable_points(2000*12)
        # self.calc_usable_points(2500*12)

    def resize_image(self):
        if max(self.original_image_size) > self.max_image_size:
            scaling_factor = self.max_image_size / max(self.original_image_size)
            new_size = (floor(scaling_factor * self.original_image_size[0]),
                        floor(scaling_factor * self.original_image_size[1]))
            self.image = self.image.resize(new_size, Image.ANTIALIAS)
            self.image.save(self.file_name)
        if self.debug:
            self.image.show()
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
        self.inch_per_pixel =  self.radius * 2 / self.image_size[0]
        print("Inch per pixel: ", self.inch_per_pixel)
        return np.meshgrid(xs, ys)

    def calc_fitness(self, peg1, peg2):
        """ See how much a given line matches the image """
        peg1_pos = np.asmatrix([self.pegs[peg1][0], self.pegs[peg1][1]])
        peg2_pos = np.asmatrix([self.pegs[peg2][0], self.pegs[peg2][1]])

        string_vector = peg2_pos - peg1_pos
        v_hat = string_vector / np.linalg.norm(string_vector)
        # unit vector perpendicular to the string vector
        v_hat_perp = (v_hat * np.asmatrix([[0, -1], [1, 0]]))
        n = self.pixel_x_coors.shape[1]
        # pixel_points has size (2 x n^2)
        pixel_points = np.concatenate((self.pixel_x_coors.reshape((1, n**2)),
                                self.pixel_y_coors.reshape((1, n**2))), axis=0)
        # vectors from every pixel to the first peg
        pixel_vectors = pixel_points - (peg1_pos.T * np.ones((1, n**2)))
        norms = v_hat_perp * np.asmatrix(pixel_vectors)
        norms = np.abs(norms.reshape((n, n)))

        #TODO: replace *7 with half the pixel-inch conversion factor
        valid_points = (norms < self.string_thickness/self.inch_per_pixel)
        fitness = np.sum(self.np_image[valid_points])
        if self.debug:
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
        self.all_lines = []
        peg_combinations = combinations(range(self.num_pegs), 2)
        for combo in peg_combinations:
            peg1, peg2 = combo;
            fitness = self.calc_fitness(peg1, peg2)
            self.all_lines.append((fitness, peg1, peg2))
            print(fitness)
        self.all_lines = sorted(self.all_lines, reverse=True)

    def calc_usable_points(self, max_length):
        """ Pick the best paths in the right order to minimize string used """
        # Returns: list of tuples. Each tuple contains a peg combo
        # (from_peg, to_peg)
        line_collection = []
        self.usable_lines = set([])
        length_used = 0
        index = 0
        while length_used < max_length:
            fitness = self.all_lines[index][0]
            peg1 = self.all_lines[index][1]
            peg2 = self.all_lines[index][2]
            peg1_points = self.pegs[peg1]
            peg2_points = self.pegs[peg2]
            index += 1
            length_used += ((peg1_points[0] - peg2_points[0])**2 + (peg1_points[1] - peg2_points[1])**2)**0.5
            print(length_used)
            self.usable_lines.add(frozenset([peg1, peg2]))
            line_collection.append([(peg1_points[0], peg1_points[1]), (peg2_points[0], peg2_points[1])])
            index += 1

        fig, ax = plt.subplots()
        ax.axis([-self.radius, self.radius, -self.radius, self.radius])
        for peg in self.pegs:
            plt.plot(peg[0], peg[1], 'ko')

        plt.axis("equal")
        lc = mc.LineCollection(line_collection, colors='k', linewidths=self.string_thickness/self.inch_per_pixel)
        ax.add_collection(lc)
        plt.show()

    def calc_optimal_path(self, max_length):
        self.calc_usable_points(max_length)
        self.peg_histogram = {}
        self.final_peg_list = []
        self.additional_length = 0
        for peg_number in range(self.num_pegs):
            # Get number of connections per peg
            self.peg_histogram[peg_number] = len([peg_number for combo in self.usable_lines if peg_number in combo])
        peg_histogram_list = sorted(self.peg_histogram.items(), key=lambda x: x[1], reverse=True)
        curr_peg = peg_histogram_list[0][0]
        total_lines = len(self.usable_lines)
        print(total_lines, 'TOTAL LINES')
        sleep(1)
        while sum(self.peg_histogram.values()) > 0:
            index = 0
            next_peg = None
            while next_peg is None:
                if frozenset([curr_peg, peg_histogram_list[index][0]]) in self.usable_lines:
                    next_peg = peg_histogram_list[index][0]
                    assert next_peg is not None
                    direct = 1
                    if self.debug: print('direct')
                elif index == len(peg_histogram_list) - 1:
                    if curr_peg == peg_histogram_list[0][0]:
                        next_peg = peg_histogram_list[1][0]
                    else:
                        next_peg = peg_histogram_list[0][0]
                    direct = 0
                    if self.debug: print('not direct')
                else:
                    index += 1
                    if self.debug: print('nada')
            self.final_peg_list.append((curr_peg, next_peg, direct))
            self.peg_histogram[curr_peg] -= 1
            self.peg_histogram[next_peg] -= 1
            if direct:
                self.usable_lines.remove(frozenset([curr_peg, next_peg]))
            else:
                self.additional_length += abs(next_peg - curr_peg) / self.num_pegs * 2 * pi * self.radius
            print(len(self.final_peg_list)/total_lines * 100, '% COMPLETE')
            peg_histogram_list = sorted(self.peg_histogram.items(), key=lambda x: x[1], reverse=True)
            curr_peg = next_peg

        print(self.additional_length)
        print(self.final_peg_list)
        self.plot_path()

    def create_cardioid(self, num_lines, order):
        self.final_peg_list = []
        final_peg_list = []
        curr_peg = 1
        for line in range(num_lines):
            next_peg = floor(curr_peg * order % self.num_pegs)
            self.final_peg_list.append((curr_peg, next_peg, 1))
            self.final_peg_list.append((curr_peg, curr_peg + 1 % self.num_pegs, 0))
            final_peg_list.append((next_peg, 1))
            final_peg_list.append(((curr_peg + 1) % self.num_pegs, 0))
            curr_peg = (curr_peg + 1) % self.num_pegs
        print(final_peg_list)
        self.plot_path()


    def plot_path(self):
        line_collection = []
        for line in self.final_peg_list:
            if line[2]:
                peg1_points = self.pegs[line[0]]
                peg2_points = self.pegs[line[1]]
                line_collection.append([(peg1_points[0], peg1_points[1]), (peg2_points[0], peg2_points[1])])

        fig, ax = plt.subplots()
        ax.axis([-self.radius, self.radius, -self.radius, self.radius])
        for i, peg in enumerate(self.pegs):
            plt.plot(peg[0], peg[1], 'ko')
        plt.axis("equal")
        lc = mc.LineCollection(line_collection, colors='k', linewidths=self.string_thickness/self.inch_per_pixel)
        ax.add_collection(lc)
        plt.show()

if __name__ == "__main__":
    test = ImageProcessor(file_name="woman.jpeg", debug=False)

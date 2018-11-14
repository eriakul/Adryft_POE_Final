import pygame
from math import floor, pi, cos, sin, hypot
from time import sleep
from operator import itemgetter
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from itertools import combinations
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, show
from simulation import *
#pip install Pillow==3.1.2
import os


class ImageProcessorJZ(ImageProcessor):
    def compute_lines(self):

        peg_combinations = combinations(range(self.peg_num), 2)
        self.line_dict = {}
        self.string_cost_dict = {}
        self.histogram = {}

        for index_set in peg_combinations:
            peg_1 = self.pegs[index_set[0]]
            peg_2 = self.pegs[index_set[1]]
            length = int(np.hypot(peg_2[0] - peg_1[0], peg_2[1] - peg_1[1]))
            xs = np.linspace(peg_1[0]-2, peg_2[0]-2, length).tolist()
            ys = np.linspace(peg_1[1]-2, peg_2[1]-2, length).tolist()
            xs = list(map(int, xs))
            ys = list(map(int, ys))

            line_fit = np.sum(self.np_image[ys, xs])
            self.line_dict[line_fit] = [index_set[0], index_set[1]]
            self.string_cost_dict[frozenset([index_set[0], index_set[1]])] = self.real_radius/(self.diameter/2)*length
            self.histogram[frozenset([index_set[0], index_set[1]])] = 0


    def compute_best_path(self):
        fitnesses = sorted(list(self.line_dict.keys()), reverse=True)

        print(type(fitnesses))
        print(fitnesses)
        
        self.current_index = self.line_dict[fitnesses[-1]][0]
        best_index = self.line_dict[fitnesses[-1]][1]
        self.line_dict.pop(fitnesses[-1])
        return best_index


if __name__ == "__main__":

    pygame.init()

    file_name = "pokeball.jpeg"

    peg_num = 90
    string_thickness = 1
    max_string = 3000
    real_radius = 1
    max_overlap = 2

    window_size = [1200, 800]



    stringomatic = System(window_size, peg_num = peg_num, string_thickness = string_thickness)
    done = False
    image = ImageProcessorJZ(file_name, peg_num = peg_num, string_thickness = string_thickness,
                            real_radius = real_radius, max_overlap = max_overlap)

    stringomatic.add_image_information(image)

    # peg_list = image.find_peg_list()
    # print(peg_list)
    # stringomatic.draw_mesh(peg_list)

    check = True #checks if string art is complete
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                file_name = file_name.split(".")[0] + "_{}_{}".format(peg_num, real_radius).replace(".", "")
                pygame.image.save(stringomatic.screen, file_name +"_result.jpeg")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    check = not check
                    if not check:
                        image.comparison_image.show()
                        image.plot_mean_squared_error()

            if event.type == pygame.MOUSEBUTTONDOWN:
                stringomatic.process_click()

        if image.total_string_cost < max_string and check:
            check = stringomatic.draw_mesh_live(image)
        else:
            sleep(.1)

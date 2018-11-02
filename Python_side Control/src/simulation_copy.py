import pygame
from math import floor, pi, cos, sin, hypot
from time import sleep
from operator import itemgetter

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

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("String Art Simulation")
        pygame.draw.circle(self.screen,
                            self.screen_properties["board_color"],
                            self.screen_properties["center"],
                            self.screen_properties["board_radius"])
        pygame.display.flip()
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

class generate_array:
    """
    Genereate a list of integers that refers to the number of the peg.
    """
    def __init__(self, number_of_pegs, length_of_generated_list, difference, peg_to_start = 0):
        self.number_of_pegs = number_of_pegs
        self.lenght = length_of_generated_list
        self.difference = difference
        self.generated_list = [peg_to_start]
        self.current_peg = peg_to_start

    def create_list(self):
        """Create list of peg array that can be used in class System.draw_mesh() to draw a draw_mesh
        """
        for i in range(self.lenght):
            self.current_peg += self.difference
            self.generated_list.append(self.current_peg)

        for j in range(len(self.generated_list)):
             self.generated_list[j] = self.generated_list[j] % self.number_of_pegs

        return self.generated_list

    def __str__(self):
        return str(self.generated_list)




if __name__ == "__main__":

    window_size = [1000, 1000]

    pygame.init()
    hello = System(window_size, peg_num = 36)
    peg_list = generate_array(hello.peg_num, length_of_generated_list = 100, difference = 13)
    hello.draw_mesh(peg_list.create_list())

    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN :
                hello.process_click()
        sleep(.05)

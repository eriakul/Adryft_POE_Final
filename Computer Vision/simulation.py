import pygame
from math import floor, pi, cos, sin
class System:
    def __init__(self, window_size, peg_num = 36, string_thickness = 1, peg_size = 2):
        self.peg_num = peg_num
        self.string_thickness = string_thickness
        self.peg_size = peg_size
        self.screen_properties = dict(
            board_color = pygame.Color(255, 255, 255, 255),
            board_radius = floor(window_size[1]/2*.9),
            center = [floor(window_size[0]/2), floor(window_size[1]/2)],
            pegs = self.create_pegs()
            )

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("String Art Simulation")
        pygame.draw.circle(self.screen,
                            self.screen_properties["board_color"],
                            self.screen_properties["center"],
                            self.screen_properties["board_radius"])
        pygame.display.flip()

    def update_window(self):
        pass

    def create_pegs(self):
        angle_steps = 2*pi/self.peg_num
        peg_locations = []
        # for i in range(0, 2*pi, angle_steps):
        #     location = []
        #     peg_locations.append()
        return angle_steps



if __name__ == "__main__":

    window_size = [1000, 500]


    pygame.init()
    hello = System(window_size)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

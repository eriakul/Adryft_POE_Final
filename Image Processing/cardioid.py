from math import floor, pi, cos
class MakeCardioidList:
    def __init__(self, num_pegs = 96):
        self.num_pegs = num_pegs
    def create_cardioid(self, num_lines, order):
        final_peg_list = []
        curr_peg = 1
        for line in range(num_lines):
            next_peg = floor(curr_peg * order % self.num_pegs)
            final_peg_list.append((next_peg, 1))
            curr_peg = (curr_peg + 1) % self.num_pegs
            final_peg_list.append((curr_peg, 0))
        return final_peg_list

machine = MakeCardioidList()
peg_list = machine.create_cardioid(50, 3)


def string_calculator(peg_list, peg_num = 96, radius = 1):
    string_used = 0
    current = 1
    theta = []
    for i in range(peg_num):
        theta.append(2*pi*i/peg_num)

    for peg in peg_list:
        next = peg[0]
        move_type = peg[1]
        if move_type == 0:
            add = sqrt( 2 * (radius**2) * (1 - cos(that[current-1]- theta[next-1])))
            string_used += add
        elif move_type == 1:

        else:
            print("ABORT")


string_calculator(peg_list)

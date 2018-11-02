

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
        for i in range(self.lenght):
            self.current_peg += self.difference
            self.generated_list.append(self.current_peg)

        for j in range(len(self.generated_list)):
             self.generated_list[j] = self.generated_list[j] % self.number_of_pegs

        return self.generated_list

    def __str__(self):
        return str(self.generated_list)


if __name__ == "__main__":
    generation = generate_array(36, 40, 7)
    new_peg_list = generation.create_list()
    print(new_peg_list)

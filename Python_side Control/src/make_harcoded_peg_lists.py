class plg():
    def __init__(self, peg_num = 48):
        self.peg_num = peg_num

    def peg(self, num):
        if num < 0 or num > self.peg_num:
            return num%self.peg_num
        else:
            return num

    def cardioid(self, steps = 50):
        order = 2
        peg_list = []
        start = 0
        for i in range(steps):
            peg_list.append(round(order * i % self.peg_num))
        return peg_list

    def heart(self):
        peg_list = []
        start = 0
        fourth = int(self.peg_num/4)
        for i in range(self.peg_num):
            curr_peg = self.peg(fourth-start)
            peg_list.append(curr_peg)
            curr_peg = self.peg(2*fourth-start)
            peg_list.append(curr_peg)
            start-=1
        return peg_list

    def spiral(self, steps = 50):
        peg_list = []
        curr_peg = 0
        step = 0
        for i in range(steps):
            curr_peg = self.peg(curr_peg + step)
            peg_list.append(curr_peg)
            step+=1
        return peg_list

gen = plg()
print(gen.cardioid())

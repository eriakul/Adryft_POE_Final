class plg():
    def __init__(self, peg_num = 48):
        self.peg_num = peg_num

    def peg(self, num):
        if num < 0 or num > self.peg_num:
            return num%self.peg_num
        else:
            return num



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
gen = plg()
print(gen.heart())

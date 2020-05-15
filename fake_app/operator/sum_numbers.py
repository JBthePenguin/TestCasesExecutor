class SumTwo():
    def __init__(self, a, b):
        self.sum = a + b

    def int_result(self):
        return int(self.sum)

    def float_resut(self):
        return float(self.sum)

    def bin_result(self):
        return bin(self.sum)


class SumThree(SumTwo):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.sum += c

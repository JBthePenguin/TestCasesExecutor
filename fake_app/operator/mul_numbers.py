class MulTwo():
    def __init__(self, a, b):
        self.mul = a * b

    def int_result(self):
        return int(self.mul)

    def float_result(self):
        return float(self.mul)

    def bin_result(self):
        return bin(self.mul)


class MulThree(MulTwo):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.mul *= c

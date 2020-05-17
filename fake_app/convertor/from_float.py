class FromFloat():
    def __init__(self, float_number):
        self.float_number = float_number

    def to_int(self):
        return int(self.float_number)

    def to_str(self):
        return str(self.float_number).replace('.', ',')

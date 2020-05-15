class FromInt():
    def __init__(self, int_number):
        self.int_number = int_number

    def to_bin(self):
        return bin(self.int_number)

    def to_hex(self):
        return hex(self.int_number)

    def to_str(self):
        return str(self.int_number)

class FromStr():
    def __init__(self, number_string):
        self.number_string = number_string

    def to_int(self):
        return int(self.number_string)

    def to_float(self):
        return float(self.number_string.replace(',', '.'))

    def to_bin(self):
        return ''.join(format(ord(i), 'b') for i in self.number_string)

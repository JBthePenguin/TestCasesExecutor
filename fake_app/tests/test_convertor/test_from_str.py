from unittest import TestCase
from fake_app.convertor.from_str import FromStr


class TestFromStr(TestCase):

    def test_to_int(self):
        self.assertEqual(FromStr('5').to_int(), 5)

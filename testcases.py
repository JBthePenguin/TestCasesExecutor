from fake_app.tests.test_convertor.test_from_str import TestFromStr
from fake_app.tests.test_convertor.test_from_int import TestFromInt
from fake_app.tests.test_convertor.test_from_float import TestFromFloat
from fake_app.tests.test_operator.test_sum_numbers import (
    TestSumTwo, TestSumThree)
from fake_app.tests.test_operator.test_mul_numbers import (
    TestMulTwo, TestMulThree)

groups = [
    ('conv', [TestFromInt, TestFromFloat, TestFromStr]),
    ('op_two', [TestSumTwo, TestMulTwo]),
    ('op_three', [TestSumTwo, TestSumThree, TestMulThree]), 2]

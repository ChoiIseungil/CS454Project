from unittest import TestCase
from quicksort import quicksort

class CalculatorTest(TestCase):

    def test1(self):
        self.assertEqual(quicksort([1, 6, 4, 3, 6, 7, 10]), [1, 3, 4, 6, 6, 7, 10])
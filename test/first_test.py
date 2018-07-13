import unittest
import calc


class TestAdd(unittest.TestCase):
    def test_add(self):
        result = calc.add(10, 5)
        self.assertEqual(result, 15)
        self.assertEqual(calc.add(15, 2), 15)


if __name__ == '__main__':
    unittest.main()
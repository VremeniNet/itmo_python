import unittest
from main import SumTwo

class TestSumTwo(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(SumTwo([2,7,11,15], 9), [0, 1])

    def test_example_2(self):
        self.assertEqual(SumTwo([3,2,4], 6), [1, 2])

    def test_example_3(self):
        self.assertEqual(SumTwo([3,3], 6), [0, 1])

    def test_empty_list(self):
        self.assertIsNone(SumTwo([], 10))

    def test_single_element(self):
        self.assertIsNone(SumTwo([5], 5))

    def test_no_solution(self):
        self.assertIsNone(SumTwo([1,2,3], 7))

    def test_zero_and_duplicates(self):
        self.assertEqual(SumTwo([0,4,0], 0), [0, 2])

    def test_negatives(self):
        self.assertEqual(SumTwo([-3, 4, 1, 2], -1), [0, 3])

    def test_large_numbers(self):
        self.assertEqual(SumTwo([10**9, -10**9 + 3, 3], 3), [0, 1])

    def test_same_number_but_need_two_indices(self):
        self.assertIsNone(SumTwo([3], 6))
        self.assertEqual(SumTwo([1,1], 2), [0, 1])

    def test_multiple_possible_pairs_returns_first_by_order(self):

        self.assertEqual(SumTwo([1,2,3,4], 5), [0, 3])

    def test_result_type_and_len(self):
        res = SumTwo([2,5,5,11], 10)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)
        self.assertEqual(res, [1, 2])

    def test_float_in_array_returns_none(self):
        self.assertIsNone(SumTwo([2.0, 7, 11, 15], 9))
        self.assertIsNone(SumTwo([2, 7, 11.0, 15], 9))
        self.assertIsNone(SumTwo([float('nan'), 7, 2], 9))
        self.assertIsNone(SumTwo([float('inf'), 7, 2], 9))

    def test_float_target_returns_none(self):
        self.assertIsNone(SumTwo([2, 7, 11, 15], 9.0))
        self.assertIsNone(SumTwo([3, 2, 4], 6.0))

if __name__ == "__main__":
    unittest.main()
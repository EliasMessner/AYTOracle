import unittest

from IPython.lib.pretty import pprint

import AYTOracle
import parser


class MyTestCase(unittest.TestCase):
    def test_simple(self):
        sp_path = "test_data/simple/sp.txt"
        mc_path = "test_data/simple/mc.txt"
        truth = parser.parse_seating_plans("test_data/simple/truth.txt")
        match_combinations = AYTOracle.get_all_possible_match_combinations_wrapper(sp_path, mc_path)
        pprint(match_combinations)
        self.assertCountEqual(match_combinations, truth)

    def test_complex(self):
        sp_path = "test_data/complex/sp.txt"
        mc_path = "test_data/complex/mc.txt"
        truth = parser.parse_seating_plans("test_data/complex/truth.txt")
        cm_path = "test_data/complex/confirmed_matches.txt"
        match_combinations = AYTOracle.get_all_possible_match_combinations_wrapper(sp_path, mc_path, cm_path)
        pprint(match_combinations)
        print(len(match_combinations))
        self.assertCountEqual(match_combinations, truth)


if __name__ == '__main__':
    unittest.main()

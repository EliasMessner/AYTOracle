from IPython.lib.pretty import pprint

import AYTOracle


def main():
    sp_path = "data/ayto_2023_sp.txt"
    mc_path = "data/ayto_2023_match_counts.txt"
    cm_path = "data/ayto_2023_matches_2.txt"
    match_combinations = AYTOracle.get_all_possible_match_combinations_wrapper(sp_path, mc_path, cm_path)
    print("Possible Match Combinations:\n\n")
    pprint(match_combinations)
    print("\n\nProbabilities:\n\n")
    match_probablities = AYTOracle.get_match_probabilities(match_combinations)
    for pair, prob in match_probablities.items():
        print(f"{pair[0]} x {pair[1]}: {prob*100} %")


if __name__ == '__main__':
    main()

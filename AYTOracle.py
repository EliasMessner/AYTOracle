import itertools

from IPython.lib.pretty import pprint
from tqdm import tqdm
from math import factorial

import parser


def get_match_probabilities(possible_match_combinations) -> dict[(str, str), float]:
    result = dict()
    for pair in set(flatten(possible_match_combinations)):
        result[pair] = len([comb for comb in possible_match_combinations if pair in comb]) \
                       / len(possible_match_combinations)
    return dict(sorted(result.items(), key=lambda item: item[1]))


def get_all_possible_match_combinations_wrapper(sp_path, mc_path, cm_path=None):
    sp = parser.parse_seating_plans(sp_path)
    match_counts = parser.parse_int_list(mc_path)
    assert len(sp) == len(match_counts)
    confirmed_matches = [] if cm_path is None else parser.parse_seating_plan_by_path(cm_path)
    match_combinations = get_all_possible_match_combinations(sp, match_counts, confirmed_matches)
    return match_combinations


def get_all_possible_match_combinations(seating_plans, all_match_counts: list[int],
                                        confirmed_matches: list[(str, str)]) -> list[set[(str, str)]]:
    confirmed_matches_set = set(confirmed_matches)
    candidates_a, candidates_b = get_candidates(seating_plans)
    candidates_a_sub, candidates_b_sub, seating_plans = subtract_confirmed_matches(seating_plans,
                                                                                   confirmed_matches_set,
                                                                                   all_match_counts)
    print(f"Candidates A ({len(candidates_a)}, {len(candidates_a_sub)}) :\n")
    pprint([c if c in candidates_a_sub else f"--{c}--" for c in candidates_a])
    print(f"\n\nCandidates B ({len(candidates_b)}, {len(candidates_b_sub)}) :\n")
    pprint([(c if c in candidates_b_sub else f"--{c}--")
            for c in candidates_b])
    result = []
    for sp in generate_all_possible_seating_plans(candidates_a_sub, candidates_b_sub):
        if match_combination_possible(sp, seating_plans, all_match_counts):
            result.append(sp.union(confirmed_matches_set))
    return result


def subtract_confirmed_matches(seating_plans, confirmed_matches_set, match_counts):
    # subtract from seating plans
    seating_plans_sub = []
    for sp, mc_index in zip(seating_plans, range(len(match_counts))):
        sp_sub = set()
        for pair in sp:
            if any(candidate in flatten(confirmed_matches_set) for candidate in pair):
                if pair in confirmed_matches_set:
                    match_counts[mc_index] -= 1
                continue
            sp_sub.add(pair)
        seating_plans_sub.append(sp_sub)
    # subtract from candidates
    candidates_a_sub, candidates_b_sub = get_candidates(seating_plans_sub)
    candidates_a_sub = [c for c in candidates_a_sub if c not in [pair[0] for pair in confirmed_matches_set]]
    candidates_b_sub = [c for c in candidates_b_sub if c not in [pair[1] for pair in confirmed_matches_set]]
    return candidates_a_sub, candidates_b_sub, seating_plans_sub


def get_candidates(seating_plans) -> (list[str], list[str]):
    result = ([], [])
    for sp in seating_plans:
        add = [sorted(list(team)) for team in list(zip(*sp))]
        result = (result[0] + add[0], result[1] + add[1])
    return remove_duplicates(result[0]), remove_duplicates(result[1])


def get_all_possible_seating_plans(candidates_a, candidates_b) -> list[set[(str, str)]]:
    result = []
    permutations = itertools.permutations(candidates_a)
    limit = 10_000_000
    i = 0
    for p in tqdm(permutations, total=min(limit, factorial(len(candidates_a)))):
        result.append(set(zip(p, candidates_b)))
        i += 1
        if i >= limit:
            break
    return result


def generate_all_possible_seating_plans(candidates_a, candidates_b):
    permutations = itertools.permutations(candidates_a)
    limit = 10_000_000
    i = 0
    for p in tqdm(permutations, total=min(limit, factorial(len(candidates_a)))):
        i += 1
        if i > limit:
            return
        yield set(zip(p, candidates_b))


def match_combination_possible(seating_plan: set[{str, str}], observed_seating_plans: list[set[(str, str)]],
                               observed_match_counts: list[int]) -> bool:
    """
    Return True iff seating_plan is possible wrt. observed_seating_plans and all_match_counts.
    seating_plan must be given as set of set.
    """
    for osp, omc in zip(observed_seating_plans, observed_match_counts):
        expected_match_count = len(seating_plan & set(osp))
        if omc != expected_match_count:
            return False
    return True


def remove_duplicates(l):
    res = []
    for x in l:
        if x in res:
            continue
        res.append(x)
    return res


def flatten(l: list[list]):
    """
    Flatten the top layer.
    """
    return [item for sublist in l for item in sublist]

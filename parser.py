def parse_seating_plans(path):
    with open(path, "r") as f:
        nights = f.read().split("\n\n")
    result = []
    for night in nights:
        result.append(parse_seating_plan(night))
    return result


def parse_seating_plan(night):
    night_set = set()
    for pair_raw in night.strip().split("\n"):
        pair_raw = pair_raw.strip()
        pair = pair_raw.split(" x ")
        night_set.add((pair[0].strip(), pair[1].strip()))
    return night_set


def parse_seating_plan_by_path(path):
    with open(path, "r") as f:
        return parse_seating_plan(f.read())


def parse_int_list(path):
    with open(path, "r") as f:
        raw = f.read()
        result = [int(i) for i in raw.split()]
    return result

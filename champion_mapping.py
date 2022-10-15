import json
from typing import List

read_file = ""
write_file = ""

format_rarity: dict = {
    "cost": 0,
    "total": 0,
    "champions": {}
}

pool: dict = {
    1: 29,
    2: 22,
    3: 18,
    4: 12,
    5: 10
}


def _load_champions() -> List[dict]:
    f = open(read_file)
    champions_data = json.load(f)
    formatted_champions = _format_champions(champions_data)
    _write_champions_to_file(formatted_champions)


def _format_champions(payload: List[dict]) -> List[dict]:
    champion_overview = {}
    # set up base structure for different rarities
    for i in range(1, 6):
        rarity_dict = format_rarity.copy()
        rarity_dict["cost"] = i
        champion_overview[i] = rarity_dict

    # Sort champions by cost and add "amount" based on cost to data.
    for champ in payload:
        cost = champ.get("cost")
        name = champ.get("name").lower()
        champ["amount"] = pool[champ["cost"]]
        champ_list = champion_overview[cost]["champions"]
        champ_list[name] = champ
        champion_overview[cost]["champions"] = champ_list

    # Sum up amount for all champions in each cost/rarity and put in "total"
    for champ_cost, overview in champion_overview.items():
        champs = overview["champions"]
        total = sum([c["amount"] for c in champs.values()])
        champion_overview[champ_cost]["total"] = total

    return champion_overview


def _write_champions_to_file(payload: dict) -> None:
    json_object = json.dumps(payload, indent=4)

    with open(write_file, "w") as outfile:
        outfile.write(json_object)


def main():
    global read_file
    global write_file
    print("Which file should I read from?: ")
    read_file = input()
    print("Which file should I write to?: ")
    write_file = input()
    _load_champions()


if __name__ == '__main__':
    main()

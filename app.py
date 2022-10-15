import json
import numpy as np

probability_by_level: dict = {
    1: {
        1: 1,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    },
    2: {
        1: 1,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    },
    3: {
        1: 0.7,
        2: 0.25,
        3: 0,
        4: 0,
        5: 0
    },
    4: {
        1: 0.55,
        2: 0.30,
        3: 0.15,
        4: 0,
        5: 0
    },
    5: {
        1: 0.45,
        2: 0.33,
        3: 0.20,
        4: 0.02,
        5: 0
    },
    6: {
        1: 0.25,
        2: 0.40,
        3: 0.30,
        4: 0.05,
        5: 0
    },
    7: {
        1: 0.19,
        2: 0.30,
        3: 0.35,
        4: 0.15,
        5: 0.01
    },
    8: {
        1: 0.15,
        2: 0.20,
        3: 0.35,
        4: 0.25,
        5: 0.05
    },
    9: {
        1: 0.10,
        2: 0.15,
        3: 0.30,
        4: 0.30,
        5: 0.15
    }
}

champion_overview: dict = {}


def _load_champion_set():
    global champion_overview
    with open("data/formatted/champions.json") as f:
        champion_overview = json.load(f)


def _ui_loop():
    global lvl
    global champion
    global amount
    print("Welcome!")
    print("This app calculates the chance of getting a certain champ on a roll.")
    print("Select a level, champion and the amount of that champion that has been removed from the champion pool.")
    print()
    while True:
        while True:
            print("Which lvl are you?")
            try:
                lvl = int(input())
                if lvl not in range(1, 10):
                    print("Lvl must be between 1 and 9, please try again.")
                    print()
                    continue
                else:
                    print()
                    break
            except Exception:
                print("Lvl must be a number, please try again.")
                print()
                continue

        while True:
            print("Which champion would you like to check?")
            champion = input()
            selected_champion = _get_champion(champion)
            if selected_champion is not None:
                print(str(selected_champion))
                print()
                break
            else:
                print(f"Champion '{champion}' was not found.")
                print("Did you spell correctly? please try again.")
                print()
                continue

        while True:
            print("How many of that champion are already taken?")
            try:
                champion_name = selected_champion["name"]
                max_champion = selected_champion["amount"]
                taken = int(input())
            except Exception:
                print("Amount must be a number, please try again.")
                print()
                continue

            if taken > max_champion:
                print(f"{taken} is too many, {champion_name} has a maximum of {max_champion} copies in the pool at any given time.")
                print("Please try again.")
                print()
                continue
            else:
                prob = _calculate_probability(lvl, selected_champion, taken)
                print(f"The probability of getting at least one {champion_name} on you next roll is {prob}%.")
                break


def _get_champion(champion: str) -> dict:
    for rarity in champion_overview.values():
        if champion in rarity["champions"]:
            return rarity["champions"][champion]

    return None


def _calculate_probability(lvl: int, champion: dict, amount: int):
    rarity = champion["cost"]
    prob_of_rarity: float = probability_by_level[lvl][rarity]
    total_by_rarity = champion_overview[str(rarity)]["total"] - amount
    champions_left = champion["amount"] - amount
    chance_of_atleast_one = np.prod([1 - (champions_left / (total_by_rarity - i))
                                     for i in range(5)])

    probability = (prob_of_rarity * (1 - (chance_of_atleast_one))) * 100
    final_probability = round(probability, 1)
    return final_probability


def main():
    _load_champion_set()
    _ui_loop()


if __name__ == '__main__':
    main()

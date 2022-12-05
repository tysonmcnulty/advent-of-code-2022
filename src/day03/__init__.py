from functools import cache


def load(data_file: str):
    rucksacks = []
    with open(data_file) as rucksacks_data:
        for line in rucksacks_data:
            item_types = line.strip()
            num_items = len(item_types)
            rucksacks.append(
                Rucksack(
                    (
                        Compartment.from_str(item_types[: int(num_items / 2)]),
                        Compartment.from_str(item_types[int(num_items / 2) :]),
                    )
                )
            )

    return rucksacks


@cache
def get_priority(type):
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".find(type) + 1


class Item:
    def __init__(self, type: str):
        self.type = type

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.type == other.type
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.type,))

    @property
    def priority(self):
        return get_priority(self.type)


class Compartment:
    def __init__(self, items: list[Item]):
        self.items = items

    def __eq__(self, other):
        if isinstance(other, Compartment):
            return self.items == other.items
        else:
            return NotImplemented

    @staticmethod
    def from_str(type_data: str):
        return Compartment(items=[Item(t) for t in type_data])


class Rucksack:
    def __init__(self, compartments: tuple[Compartment, Compartment]):
        self.compartments = compartments

    def __eq__(self, other):
        if isinstance(other, Rucksack):
            return self.compartments == other.compartments
        else:
            return NotImplemented

    @property
    def first_compartment(self):
        return self.compartments[0]

    @property
    def second_compartment(self):
        return self.compartments[1]

    @property
    def items(self):
        return self.first_compartment.items + self.second_compartment.items


def get_unsorted_item(rucksack: Rucksack):
    return next(
        iter(
            set(rucksack.first_compartment.items).intersection(
                set(rucksack.second_compartment.items)
            )
        )
    )


def get_badges(rucksacks: list[Rucksack]) -> list[Item]:
    badges = []
    for i in range(0, len(rucksacks), 3):
        badges.append(
            next(
                iter(
                    set(rucksacks[i].items).intersection(
                        set(rucksacks[i + 1].items), set(rucksacks[i + 2].items)
                    )
                )
            )
        )

    return badges

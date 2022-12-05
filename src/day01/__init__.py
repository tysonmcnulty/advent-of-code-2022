def load(data_file: str):
    elves = []
    with open(data_file) as calorie_data:
        calorie_counts = []
        for line in calorie_data:
            if line.isspace():
                elves.append(Elf([FoodItem(ct) for ct in calorie_counts]))
                calorie_counts = []
            else:
                calorie_counts.append(int(line.strip()))

    if len(calorie_counts) > 0:
        elves.append(Elf([FoodItem(ct) for ct in calorie_counts]))

    return elves


class FoodItem:
    def __init__(self, calorie_count: int):
        self.calorie_count = calorie_count

    def __eq__(self, other):
        if isinstance(other, FoodItem):
            return self.calorie_count == other.calorie_count
        else:
            return NotImplemented

    def __str__(self):
        return f"{self.calorie_count}"

    def __repr__(self):
        return f"FoodItem({str(self)})"


class Elf:
    def __init__(self, food_items: list[FoodItem]):
        self.food_items = food_items

    def __eq__(self, other):
        if isinstance(other, Elf):
            return self.food_items == other.food_items
        else:
            return NotImplemented

    def __str__(self):
        return f"{self.food_items}"

    def __repr__(self):
        return f"Elf({str(self)})"


def elf_calorie_count(elf: Elf):
    return sum([f.calorie_count for f in elf.food_items])


def get_max_elf_calorie_count(elves: list[Elf]):
    return max([elf_calorie_count(elf) for elf in elves])


def get_top_three_elf_calorie_counts(elves: list[Elf]):
    return sorted([elf_calorie_count(elf) for elf in elves], reverse=True)[:3]

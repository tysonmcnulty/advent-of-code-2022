from pathlib import Path


def load_data(data_file: Path) -> list[str]:
    with open(data_file) as data:
        return [*data]

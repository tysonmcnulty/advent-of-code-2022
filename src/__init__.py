def load_data(data_file: str) -> list[str]:
    with open(data_file) as data:
        return [*data]

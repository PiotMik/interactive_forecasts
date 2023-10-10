import os
import pandas as pd
import json
import pathlib

DATA_PATH = pathlib.Path(r"D:\piter\Python Scripts\interactive_forecasts\data")


def load_data(name: str) -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH / f"{name}.csv", index_col=0)
    data.index = pd.PeriodIndex(data.index, freq="M")
    return data


def dump_data(data: pd.DataFrame, name: str) -> None:
    data.to_csv(DATA_PATH / f"{name}.csv")


class Cache:

    def __init__(self):
        self.handle = DATA_PATH / "cache.json"

    def is_empty(self):
        return os.stat(self.handle).st_size == 0

    def create(self):
        self.handle.touch()

    def delete(self) -> None:
        if self.handle.exists():
            self.handle.unlink()

    def read(self) -> dict:
        if self.is_empty():
            current_cache = {}
        else:
            with open(self.handle, "r") as cache_file:
                current_cache = json.load(cache_file)
        return current_cache

    def write(self, data: dict = None):
        if data is None:
            data = {}
        current_cache = self.read()
        current_cache.update(data)
        with open(self.handle, "w") as cache_file:
            json.dump(current_cache, cache_file)


if __name__ == "__main__":
    pass

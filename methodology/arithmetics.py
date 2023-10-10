import pandas as pd


def shift_data(dataset: pd.DataFrame, scalar: float) -> pd.DataFrame:
    return dataset + scalar


def multiply(dataset: pd.DataFrame, scalar: float) -> pd.DataFrame:
    return dataset * scalar


if __name__ == '__main__':
    pass

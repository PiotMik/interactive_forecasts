import pandas as pd


def expert_judgement(dataset: pd.DataFrame, variable: str, date: pd.Period, value: float):
    dataset.loc[variable, date] = value
    return dataset


if __name__ == "__main__":
    pass

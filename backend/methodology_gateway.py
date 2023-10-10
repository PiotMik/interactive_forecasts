import methodology
from backend import data_management
import typing
import abc
import pandas as pd


class MethodologyWrapper(abc.ABC):

    def __init__(self, logic: typing.Callable):
        self.logic = logic

    @abc.abstractmethod
    def prepare_inputs(self, **kwargs) -> dict:
        pass

    def call(self, **kwargs):
        return self.logic(**kwargs)

    @classmethod
    def get_wrapper(cls, methodology_name):
        wrappers = {methodology.simple_mapping.__name__: SimpleMappingsWrapper(logic=methodology.simple_mapping),
                    methodology.multiply.__name__: ArithmeticWrapper(logic=methodology.multiply),
                    methodology.shift_data.__name__: ArithmeticWrapper(logic=methodology.shift_data)}
        return wrappers[methodology_name]


class SimpleMappingsWrapper(MethodologyWrapper):
    @classmethod
    def prepare_inputs(cls, dataset: str,
                       explanatory_series: str, explained_series: str,
                       mapping: dict, date: str):
        data = data_management.load_data(dataset)
        explanatory_series, explained_series = data[explanatory_series], data[explained_series]
        mapping = methodology.simple_mappings.MappingConfig(**mapping)
        date = pd.Period(date)
        return {'explanatory_series': explanatory_series,
                'explained_series': explained_series,
                'mapping': mapping,
                'date': date}


class ArithmeticWrapper(MethodologyWrapper):
    @classmethod
    def prepare_inputs(cls, dataset: str, scalar: float):
        data = data_management.load_data(dataset)
        return {'dataset': data,
                'scalar': scalar}


if __name__ == '__main__':
    pass

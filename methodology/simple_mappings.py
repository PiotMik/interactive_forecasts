from enum import Enum
from pydantic import BaseModel
import pandas as pd


class MappingType(Enum):
    RELATIVE = "percentage growth"
    ABSOLUTE = "absolute growth"

    @property
    def transform(self):
        transform_map = {self.RELATIVE: lambda ts, **kwargs: ts.pct_change(**kwargs),
                         self.ABSOLUTE: lambda ts, **kwargs: ts.diff(**kwargs)}
        return transform_map[self]

    @property
    def apply(self):
        transform_map = {self.RELATIVE: lambda jumpoff, growth: jumpoff * (1 + growth),
                         self.ABSOLUTE: lambda jumpoff, growth: jumpoff + growth}
        return transform_map[self]


class MappingPeriod(Enum):
    MoM = "MoM"
    QoQ = "QoQ"
    YoY = "YoY"

    @property
    def period_str(self):
        return self.value[0]

    @property
    def n_months(self):
        return {self.MoM: 1,
                self.QoQ: 3,
                self.YoY: 12}[self]


class MappingConfig(BaseModel):
    period: MappingPeriod
    type: MappingType


def simple_mapping(explanatory_series: pd.Series, explained_series: pd.Series,
                   mapping: MappingConfig, date: pd.Period):
    results = {}
    for series, role in zip([explained_series, explanatory_series],
                            ["explained", "explanatory"]):
        series = series[:date]
        transformed = mapping.type.transform(series, periods=mapping.period.n_months)
        growth = transformed[date]
        jumpoff = series[date - mapping.period.n_months]
        results[role] = {"jumpoff": jumpoff, "growth": growth}

    forecast = mapping.type.apply(jumpoff=results['explained']['jumpoff'],
                                  growth=results['explanatory']['growth'])
    explained_series[date] = forecast
    return_df = explained_series.to_frame().loc[[date]].copy()
    return return_df

if __name__ == "__main__":
    pass

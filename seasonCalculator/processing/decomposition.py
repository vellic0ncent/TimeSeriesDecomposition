from functools import reduce
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import linregress


class Decomposer:
    dates_column = "Date"
    time_series_column = "SebTotalSellout"
    drop_from_index = ["GroupSapEn", "GroupSapRu"]

    def __init__(self, dataframe: pd.DataFrame, freq: int):
        self.data = dataframe.droplevel(self.drop_from_index)
        self.data.sort_index(inplace=True, ascending=True)
        self.ys = self.data.SebTotalSellout.values
        self.xs = [x for x in range(1, len(self.ys) + 1)]
        self.freq = freq  # frequency => for "W" 52 is expected
        self.slope = None
        self.decomposition = None

    def show_head(self, top_n: int) -> pd.DataFrame:
        return self.data.head(top_n)

    def extract_amplitudes(self) -> np.array:
        periods = int(len(self.xs) / self.freq)
        amplitudes: np.array = []
        lower_bound_idx = 0
        for i in range(0, periods):
            amplitudes.append(max(self.xs[lower_bound_idx: lower_bound_idx + self.freq]) -
                              min(self.xs[lower_bound_idx: lower_bound_idx + self.freq]))
            lower_bound_idx += self.freq
        return amplitudes

    def define_decomposition_model(self) -> str:
        amplitudes = self.extract_amplitudes()
        flags = []
        for i in range(1, len(amplitudes)):
            flags.append(1 if amplitudes[i] > amplitudes[i - 1] else 0)

        if np.all(flags == 1) | np.all(flags == 0):
            return "multiplicative"
        else:
            return "additive"

    def decompose(self):
        try:
            return seasonal_decompose(x=self.ys, model=self.define_decomposition_model(), period=self.freq)
        except ValueError:  # if cycles are not complete
            pass

    def linear_reg(self, y_series: np.array, x_series: np.array = None) -> np.array:
        slope, intercept, rvalue, pvalue, stderr = linregress(x_series, y_series)
        self.slope = slope
        predictions: np.array = [intercept + self.slope * x for x in self.xs]
        return predictions

    def transform_trend_component(self, decomposition) -> pd.DataFrame:
        trend_with_timeline = np.array([self.xs, decomposition.trend]).transpose()
        x_series, y_series = trend_with_timeline[~np.isnan(trend_with_timeline).any(axis=1)].transpose()
        predictions = self.linear_reg(x_series=x_series, y_series=y_series)

        predictions_with_timeline = pd.DataFrame(
            {
                "date": pd.Series(data=self.data.index),
                "xs": pd.Series(data=self.xs, dtype=np.dtype("int64")),
                "predictions": pd.Series(data=predictions, dtype=np.dtype("float")),
                "decomposition_trend": pd.Series(data=decomposition.trend, dtype=np.dtype("float")),
            }
        )
        predictions_with_timeline["decomposition_trend"] = predictions_with_timeline["decomposition_trend"].fillna(
            predictions_with_timeline.pop("predictions"))

        return predictions_with_timeline

    def transform_seasonal_component(self, decomposition) -> pd.DataFrame:

        return pd.DataFrame({
            "date": pd.Series(data=self.data.index),
            "xs": pd.Series(data=self.xs, dtype=np.dtype("int64")),
            "decomposition_seasonal": pd.Series(data=decomposition.seasonal, dtype=np.dtype("float")),
        })

    def transform_residual_component(self, decomposition) -> pd.DataFrame:
        model_type = self.define_decomposition_model()
        trend_component = self.transform_trend_component(decomposition)["decomposition_trend"]
        seasonal_component = self.transform_seasonal_component(decomposition)["decomposition_seasonal"]
        if model_type == "multiplicative":
            residual_component = self.ys / np.array(trend_component) / np.array(seasonal_component)
        elif model_type == "additive":
            residual_component = self.ys - np.array(trend_component) - np.array(seasonal_component)
        else:
            raise KeyError

        return pd.DataFrame({
            "date": pd.Series(data=self.data.index),
            "xs": pd.Series(data=self.xs, dtype=np.dtype("int64")),
            "decomposition_residual": pd.Series(data=residual_component, dtype=np.dtype("float")),
        })

    def extract_components(self) -> pd.DataFrame:
        try:
            decomposition = self.decompose()
            self.decomposition = decomposition

            components = [
                self.transform_trend_component(decomposition=decomposition),
                self.transform_seasonal_component(decomposition=decomposition),
                self.transform_residual_component(decomposition=decomposition)
            ]
            return reduce(lambda left, right: pd.merge(left, right, on=['xs', 'date']), components).drop(
                columns=['xs']
            )
        except AttributeError:
            pass

    def extract_slope(self) -> float:
        try:
            return self.slope
        except AttributeError:
            pass

    def extract_growth_rate(self) -> float:
        try:
            trend = self.transform_trend_component(decomposition=self.decomposition)["decomposition_trend"]
            minimum = min(trend)
            trend += abs(minimum) * 1.5
            return (trend.iloc[-1] - trend.iloc[0]) / trend.iloc[0]
        except AttributeError:
            pass

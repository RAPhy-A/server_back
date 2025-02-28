from typing import List
import numpy as np
from scipy.interpolate import interp1d
from Cycle import Cycle

class CycleLineaire(Cycle):
    def __init__(self, time_start: float, time_end: float, value_start: float, value_end: float):
        self.time_start = time_start
        self.time_end = time_end
        self.value_start = value_start
        self.value_end = value_end
        self.f = interp1d([time_start, time_end], [value_start, value_end], kind='linear', fill_value="extrapolate")

    def get_values(self, xi: List[float]) -> List[float]:
        xi_arr = np.array(xi)
        yi = self.f(xi_arr)
        return yi.tolist()

    def get_value(self, x: float) -> float:
        return float(self.f(x))

from typing import List
from Cycle import Cycle

class CycleCombinaison(Cycle):
    def __init__(self, c1: Cycle, c2: Cycle):
        self.time_start = c1.time_start
        self.time_end = c2.time_end
        self.value_start = c1.value_start
        self.value_end = c2.value_end
        self.c1 = c1
        self.c2 = c2

    def get_values(self, xi: List[float]) -> List[float]:
        split_index = len(xi)
        for i, x in enumerate(xi):
            if x >= self.c1.time_end:
                split_index = i
                break
        xi_c1 = xi[:split_index]
        xi_c2 = xi[split_index:]
        values_c1 = self.c1.get_values(xi_c1)
        values_c2 = self.c2.get_values(xi_c2)
        return values_c1 + values_c2

    def get_value(self, x: float) -> float:
        if x < self.c1.time_end:
            return self.c1.get_values([x])[0]
        else:
            return self.c2.get_values([x])[0]
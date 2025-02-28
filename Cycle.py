from abc import ABC, abstractmethod
from typing import List

class Cycle(ABC):
    def __init__(self, time_start: float = 0.0, time_end: float = 0.0,
                 value_start: float = 0.0, value_end: float = 0.0):
        self.time_start = time_start
        self.time_end = time_end
        self.value_start = value_start
        self.value_end = value_end

    @abstractmethod
    def get_values(self, xi: List[float]) -> List[float]:
        pass

    @abstractmethod
    def get_value(self, x: float) -> float:
        pass

    def get_time_start(self) -> float:
        return self.time_start

    def get_time_end(self) -> float:
        return self.time_end

    def get_value_start(self) -> float:
        return self.value_start

    def get_value_end(self) -> float:
        return self.value_end

import time
from typing import List
from Cycle import Cycle
from GeneratorCycleRespi import GeneratorCycleRespi
from GeneratorCycleCardiaque import GeneratorCycleCardiaque
from GeneratorCycleDiurese import GeneratorCycleDiurese

class GestionCyclesLapin:
    def __init__(self):
        self.gene_resp = GeneratorCycleRespi()
        self.gene_card = GeneratorCycleCardiaque()
        self.gene_diu = GeneratorCycleDiurese()

        # Listes de cycles pour chaque modalité
        self.cycles_respiration: List[Cycle] = []
        self.cycles_cardiaque: List[Cycle] = []
        self.cycles_diurese: List[Cycle] = []

    def get_vitals(self, time_serie: List[float]) -> List[List[float]]:
        # Retourne une liste contenant les tuples [time, value_respi, value_cardiaque, value_diurese]
        vitals = []
        for t in time_serie:
            resp = self.get_value_for_cycle(t, self.cycles_respiration, self.gene_resp, 0)
            card = self.get_value_for_cycle(t, self.cycles_cardiaque, self.gene_card, 100)
            diur = self.get_value_for_cycle(t, self.cycles_diurese, self.gene_diu, 0)
            vitals.append([t, resp, card, diur])
        return vitals

    def get_value_for_cycle(self, t: float, cycles: List[Cycle], generator, default_value: float) -> float:
        # Vérifie si un cycle couvre t, sinon en génère un nouveau
        for cycle in cycles:
            if t >= cycle.get_time_start() and t <= cycle.get_time_end():
                return cycle.get_value(t)
        if isinstance(generator, GeneratorCycleRespi):
            new_cycle = generator.get_cycle(t, default_value)
        elif isinstance(generator, GeneratorCycleCardiaque):
            new_cycle = generator.get_cycle(t, default_value)
        else:  # Diurèse
            new_cycle = generator.get_cycle(t, default_value)
        cycles.append(new_cycle)
        return new_cycle.get_value(t)

    def inject_acetylcholine(self) -> None:
        current_time = time.time() * 1000  # Temps actuel en ms
        print("Injection Ace at:", current_time)
        self.gene_card.set_time_injection_ace(current_time)
        self.gene_diu.set_time_injection_ace(current_time)
        self.gene_resp.set_time_injection_ace(current_time)

from CycleLineaire import CycleLineaire
from CycleCombinaison import CycleCombinaison
from Cycle import Cycle

class GeneratorCycleDiurese:
    def __init__(self):
        self.dpm = 18
        self.duree_diusere = 60000 / self.dpm  # 3333.33 ms
        self.duree_pic_diurese = 53  # en ms

        self.pic_diurese = 1000
        self.bottom_diurese = 0

        self.time_injection_ace_diu = None  # None représente "non défini"
        self.duree_injection_ace_diu = 210000

        self.time_injection_adre_diu = None
        self.duree_injection_adre_diu = 210000

    def get_next_cycle(self, time_start: float, value_start: float) -> Cycle:
        # Cycle injection de diurèse : variation linéaire de la fréquence
        # Variation attendue : 0 à 70000 ms de 18 -> 0,
        # 70000 à 150000 ms constant à 0,
        # 150000 à 210000 ms de 0 -> 18
        if (self.time_injection_ace_diu is not None and 
            (time_start - self.time_injection_ace_diu) < self.duree_injection_ace_diu):
            avancement = time_start - self.time_injection_ace_diu
            if avancement < 70000:
                self.dpm = 18 * (70000 - avancement) / 90000.0
            elif avancement < 150000:
                self.dpm = 0
            else:
                self.dpm = min(18, 18 * avancement / 210000.0)
            self.recalculate_diusere()
            print(f"{self.duree_diusere} dpm : {self.dpm}")
        c1 = CycleLineaire(time_start, time_start + self.duree_pic_diurese, self.pic_diurese, self.pic_diurese)
        c2 = CycleLineaire(time_start + self.duree_pic_diurese, time_start + self.duree_diusere, self.bottom_diurese, self.bottom_diurese)
        return CycleCombinaison(c1, c2)

    def set_time_injection_ace(self, time: float) -> None:
        self.time_injection_ace_diu = time

    def set_time_injection_adre(self, time: float) -> None:
        self.time_injection_adre_diu = time

    def recalculate_diusere(self) -> None:
        if self.dpm <= 0.5:
            self.duree_diusere = 3000
            self.pic_diurese = 0
        else:
            self.pic_diurese = 1000
            self.duree_diusere = 60000 / self.dpm

    def get_cycle(self, time_start: float, value_start: float) -> Cycle:
        return self.get_next_cycle(time_start, value_start)

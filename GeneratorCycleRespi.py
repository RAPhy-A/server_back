from CycleLineaire import CycleLineaire
from CycleCombinaison import CycleCombinaison
from Cycle import Cycle

class GeneratorCycleRespi:
    def __init__(self):
        self.rpm = 50
        self.duree_respi = 60000 / self.rpm  # 1200 ms
        self.duree_inspi = 500  # en ms
        self.spi_basse = -40
        self.spi_haut = 40
        self.time_injection_ace_respi = None  # None représente "non défini"
        self.duree_injection_ace_respi = 250000
        self.time_injection_adre_respi = None
        self.duree_injection_adre_respi = 400000

    def get_next_cycle(self, time_start: float, value_start: float) -> Cycle:
        if (self.time_injection_ace_respi is not None and
            (time_start - self.time_injection_ace_respi) < self.duree_injection_ace_respi):
            elapsed = time_start - self.time_injection_ace_respi
            current_duree_inspi = self.duree_inspi
            if elapsed < 150000:
                current_rpm = 50 + (75 - 50) * (elapsed / 150000.0)
                if elapsed < 25000:
                    current_spi_haut = 40 + (35 - 40) * (elapsed / 25000.0)
                    current_spi_basse = -40 + ((-35) - (-40)) * (elapsed / 25000.0)
                elif elapsed < 75000:
                    current_spi_haut = 35 + (45 - 35) * ((elapsed - 25000) / 50000.0)
                    current_spi_basse = -35 + ((-45) - (-35)) * ((elapsed - 25000) / 50000.0)
                else:
                    current_spi_haut = 45 + (40 - 45) * ((elapsed - 75000) / 75000.0)
                    current_spi_basse = -45 + ((-40) - (-45)) * ((elapsed - 75000) / 75000.0)
            elif elapsed < 250000:
                current_rpm = 75 + (50 - 75) * ((elapsed - 150000) / 100000.0)
                current_spi_haut = 40
                current_spi_basse = -40
            else:
                current_rpm = self.rpm
                current_spi_haut = self.spi_haut
                current_spi_basse = self.spi_basse

            current_duree_respi = 60000 / current_rpm
            c1 = CycleLineaire(time_start, time_start + current_duree_inspi / 2, value_start, current_spi_haut)
            c2 = CycleLineaire(time_start + current_duree_inspi / 2, time_start + current_duree_inspi, current_spi_haut, 0)
            duree_expi = current_duree_respi - current_duree_inspi
            c3 = CycleLineaire(time_start + current_duree_inspi, time_start + current_duree_inspi + duree_expi / 2, 0, current_spi_basse)
            c4 = CycleLineaire(time_start + current_duree_inspi + duree_expi / 2, time_start + current_duree_respi, current_spi_basse, 0)
            return CycleCombinaison(CycleCombinaison(c1, c2), CycleCombinaison(c3, c4))

        if (self.time_injection_adre_respi is not None and
            (time_start - self.time_injection_adre_respi) < self.duree_injection_adre_respi):
            return self.get_normal_cycle(time_start, value_start)

        return self.get_normal_cycle(time_start, value_start)

    def get_normal_cycle(self, time_start: float, value_start: float) -> Cycle:
        c1 = CycleLineaire(time_start, time_start + self.duree_inspi / 2, value_start, self.spi_haut)
        c2 = CycleLineaire(time_start + self.duree_inspi / 2, time_start + self.duree_inspi, self.spi_haut, 0)
        c3 = CycleLineaire(time_start + self.duree_inspi,
                           time_start + self.duree_inspi + (self.duree_respi - self.duree_inspi) / 2, 0, self.spi_basse)
        c4 = CycleLineaire(time_start + self.duree_inspi + (self.duree_respi - self.duree_inspi) / 2,
                           time_start + self.duree_respi, self.spi_basse, 0)
        return CycleCombinaison(CycleCombinaison(c1, c2), CycleCombinaison(c3, c4))

    def set_time_injection_ace(self, time: float) -> None:
        self.time_injection_ace_respi = time

    def set_time_injection_adre(self, time: float) -> None:
        self.time_injection_adre_respi = time

    def get_cycle(self, time_start: float, value_start: float) -> Cycle:
        return self.get_next_cycle(time_start, value_start)

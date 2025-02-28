from CycleLineaire import CycleLineaire
from CycleCombinaison import CycleCombinaison
from Cycle import Cycle

class GeneratorCycleCardiaque:
    def __init__(self):
        # Paramètres normaux
        self.bpm = 150
        self.duree_battement = 60000 / self.bpm  # 400ms pour 150 bpm
        self.duree_first_pic = 18  # en ms

        self.pa_basse = 100
        self.pa_haut = 120

        # Variables injection pour l’acétylcholine (ace) et l’adréline (adre)
        self.time_injection_ace_card = None 
        self.duree_injection_ace_pa = 160000
        self.duree_injection_ace_fr = 160000

        self.time_injection_adre_card = None
        self.duree_injection_adre_fr = 220000
        self.duree_injection_adre_pa = 500000

    def set_time_injection_ace(self, time: float) -> None:
        self.time_injection_ace_card = time

    def set_time_injection_adre(self, time: float) -> None:
        self.time_injection_adre_card = time

    def get_next_cycle(self, time_start: float, value_start: float) -> Cycle:
        c1 = CycleLineaire(time_start, time_start + self.duree_first_pic, value_start, self.pa_haut)
        c2 = CycleLineaire(time_start + self.duree_first_pic, time_start + self.duree_battement, self.pa_haut, self.pa_basse)
        return CycleCombinaison(c1, c2)

    def get_cycle(self, time_start: float, value_start: float) -> Cycle:
        # Injection d'acétylcholine (ace)
        if (self.time_injection_ace_card is not None and
            (time_start - self.time_injection_ace_card) < self.duree_injection_ace_fr):
            avancement = time_start - self.time_injection_ace_card
            current_pa_basse = self.pa_basse
            current_pa_haut = self.pa_haut

            if avancement < 5000:
                # 0 à 5000 ms : pa_basse de 100 -> 85, pa_haut de 120 -> 110
                current_pa_basse = 100 + (85 - 100) * (avancement / 5000.0)
                current_pa_haut = 120 + (110 - 120) * (avancement / 5000.0)
            elif avancement < 50000:
                # 5000 à 50000 ms : pa_basse de 85 -> 80, pa_haut reste à 110
                current_pa_basse = 85 + (80 - 85) * ((avancement - 5000) / 45000.0)
                current_pa_haut = 110
            else:
                # 50000 à 160000 ms : pa_basse de 80 -> 100, pa_haut de 110 -> 120
                current_pa_basse = 80 + (100 - 80) * ((avancement - 50000) / (160000 - 50000.0))
                current_pa_haut = 110 + (120 - 110) * ((avancement - 50000) / (160000 - 50000.0))

            current_bpm = self.bpm
            if avancement < 40000:
                # 0 à 40000 ms : de 150 bpm -> 185 bpm
                current_bpm = 150 + (185 - 150) * (avancement / 40000.0)
            elif avancement < 90000:
                # 40000 à 90000 ms : constant à 185 bpm
                current_bpm = 185
            else:
                # 90000 à 160000 ms : de 185 bpm -> 150 bpm
                current_bpm = 185 + (150 - 185) * ((avancement - 90000) / (160000 - 90000.0))
            current_duree_battement = 60000 / current_bpm

            c1 = CycleLineaire(time_start, time_start + self.duree_first_pic, value_start, current_pa_haut)
            c2 = CycleLineaire(time_start + self.duree_first_pic, time_start + current_duree_battement, current_pa_haut, current_pa_basse)
            return CycleCombinaison(c1, c2)
        else:
            return self.get_next_cycle(time_start, value_start)

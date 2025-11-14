class FeuRouge:
    def __init__(self, cycle=5):
        """
        cycle : durée totale du cycle en secondes
        """
        self.cycle = cycle
        self.temps = 0

        self.duree_rouge = 0.5 * cycle
        self.duree_vert = 0.4 * cycle
        self.duree_orange = 0.1 * cycle

    @property
    def etat(self):
        """
        Retourne l'état actuel du feu parmi :
        'rouge', 'vert', 'orange'
        """
        t = self.temps % self.cycle

        if t < self.duree_rouge:
            return "rouge"
        elif t < self.duree_rouge + self.duree_vert:
            return "vert"
        else:
            return "orange"

    def avancer_temps(self, dt):
        """
        Avance le temps de dt secondes
        """
        self.temps += dt

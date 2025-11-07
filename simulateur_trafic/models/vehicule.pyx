# cython: language_level=3
# vehicule.pyx

from typing import Optional

cdef class Vehicule:
    """
    Représente un véhicule circulant sur le réseau routier, optimisé par Cython.
    """

    cdef public double position
    cdef public double vitesse
    cdef public double vitesse_max
    cdef public double distance_parcourue
    cdef public double temps_trajet

    cdef public object route_actuelle
    cdef public str identifiant

    _compteur_id = 0

    def __init__(self, vitesse_initiale: float = 0.0, position_initiale: float = 0.0,
                 route_actuelle=None):
        """
        Initialise un nouveau véhicule.
        """
        Vehicule._compteur_id += 1
        self.identifiant = f"VEH_{Vehicule._compteur_id:04d}"
        self.position = position_initiale
        self.vitesse = vitesse_initiale
        self.route_actuelle = route_actuelle
        self.vitesse_max = 130.0  # km/h
        self.distance_parcourue = 0.0
        self.temps_trajet = 0.0  # en minutes

    cpdef avancer(self, double delta_t) except*:
        """
        Fait avancer le véhicule selon sa vitesse actuelle.
        (delta_t est un float C: double)
        """
        cdef double delta_h
        cdef double vitesse_effective
        cdef double deplacement

        if self.route_actuelle is None:
            return

        delta_h = delta_t / 60.0  # Temps en heures

        vitesse_effective = min(self.vitesse, self.route_actuelle.limite_vitesse, self.vitesse_max)

        deplacement = vitesse_effective * delta_h

        self.position += deplacement
        self.distance_parcourue += deplacement
        self.temps_trajet += delta_t

        if self.position >= self.route_actuelle.longueur:
            self.position = self.route_actuelle.longueur

    def changer_de_route(self, nouvelle_route) -> bool:
        """
        Transfère le véhicule vers une nouvelle route (Méthode de gestion, reste en Python/C-appelable).
        """
        if nouvelle_route is None:
            return False

        if self.route_actuelle is not None:
            # Appel à la méthode Python Route.retirer_vehicule
            self.route_actuelle.retirer_vehicule(self)

        self.route_actuelle = nouvelle_route
        self.position = 0.0
        # Appel à la méthode Python Route.ajouter_vehicule
        nouvelle_route.ajouter_vehicule(self)

        return True

    cpdef ajuster_vitesse(self, vehicule_devant=None, double distance_securite = 0.05) except*:
        """
        Ajuste la vitesse en fonction du véhicule devant (logique réintégrée en C).
        """
        cdef double distance
        cdef double v_devant
        cdef double p_devant

        if self.route_actuelle is None:
            return

        if vehicule_devant is None:
            p_devant = -1.0
        else:
            p_devant = vehicule_devant.position  # Accès aux attributs C-déclarés de l'autre objet Vehicule
            v_devant = vehicule_devant.vitesse

        if p_devant < 0:
            self.vitesse = min(self.vitesse + 10, self.route_actuelle.limite_vitesse, self.vitesse_max)
            return

        distance = p_devant - self.position

        if distance < distance_securite:

            self.vitesse = max(0.0, v_devant - 10)
        elif distance < distance_securite * 2:

            self.vitesse = v_devant
        else:

            self.vitesse = min(self.vitesse + 5, self.route_actuelle.limite_vitesse, self.vitesse_max)

    def est_arrive(self) -> bool:
        """
        Vérifie si le véhicule a atteint la fin de sa route.
        """
        if self.route_actuelle is None:
            return False
        return self.position >= self.route_actuelle.longueur

    def __repr__(self) -> str:
        return (f"Vehicule({self.identifiant}, pos={self.position:.2f}km, "
                f"vitesse={self.vitesse:.1f}km/h)")

    def __str__(self) -> str:
        route_nom = self.route_actuelle.nom if self.route_actuelle else "Aucune"
        return (f"{self.identifiant}: {self.vitesse:.1f}km/h sur {route_nom} "
                f"(position: {self.position:.2f}km)")
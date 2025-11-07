
from typing import Optional
import numba


@numba.jit(cache=True)
def calculer_nouvelle_vitesse(vitesse: float, position: float, limite_vitesse: float,
                              vitesse_max: float, vehicule_devant_vitesse: float,
                              vehicule_devant_position: float) -> float:
    """
    Logique d'ajustement de vitesse optimisée par Numba.
    Travaille uniquement sur des types numériques.
    """

    distance_securite = 0.05


    if vehicule_devant_position < 0:
        return min(vitesse + 10, limite_vitesse, vitesse_max)


    distance = vehicule_devant_position - position

    if distance < distance_securite:
        return max(0.0, vehicule_devant_vitesse - 10)
    elif distance < distance_securite * 2:
        return vehicule_devant_vitesse
    else:
        return min(vitesse + 5, limite_vitesse, vitesse_max)

class Vehicule:
    """
    Représente un véhicule circulant sur le réseau routier.
    """

    _compteur_id = 0
    
    def __init__(self, vitesse_initiale: float = 0.0, position_initiale: float = 0.0, 
                 route_actuelle=None):
        """
        Initialise un nouveau véhicule.
        
        Args:
            vitesse_initiale: Vitesse de départ en km/h
            position_initiale: Position de départ sur la route en km
            route_actuelle: Référence à la route sur laquelle se trouve le véhicule
        """
        Vehicule._compteur_id += 1
        self.identifiant = f"VEH_{Vehicule._compteur_id:04d}"
        self.position = position_initiale
        self.vitesse = vitesse_initiale
        self.route_actuelle = route_actuelle
        self.vitesse_max = 130.0  # km/h
        self.distance_parcourue = 0.0
        self.temps_trajet = 0.0  # en minutes

    def avancer(self, delta_t: float) -> None:
        """
        Fait avancer le véhicule selon sa vitesse actuelle.

        Args:
            delta_t: Intervalle de temps en minutes
        """
        try:
            if self.route_actuelle is None:
                return

            if self.vitesse < 0:
                raise ValueError(f"Vitesse négative détectée : {self.vitesse} km/h")

            delta_h = delta_t / 60.0

            vitesse_effective = min(self.vitesse, self.route_actuelle.limite_vitesse, self.vitesse_max)

            deplacement = vitesse_effective * delta_h

            self.position += deplacement

            if self.position < 0:
                raise ValueError(f"Position invalide détectée : {self.position} km")

            self.distance_parcourue += deplacement
            self.temps_trajet += delta_t

            if self.position >= self.route_actuelle.longueur:
                self.position = self.route_actuelle.longueur

        except ValueError as e:
            print(f"Erreur lors de l’avancement du véhicule : {e}")
        except AttributeError as e:
            print(f"Erreur d’attribut: route_actuelle manquante ou invalide : {e}")
        except Exception as e:
            print(f"Erreur inattendue lors de l’avancement : {e}")


    def changer_de_route(self, nouvelle_route) -> bool:
        """
        Transfère le véhicule vers une nouvelle route.
        
        Args:
            nouvelle_route: La route de destination
            
        Returns:
            True si le changement a réussi, False sinon
        """
        if nouvelle_route is None:
            return False

        if self.route_actuelle is not None:
            self.route_actuelle.retirer_vehicule(self)

        self.route_actuelle = nouvelle_route
        self.position = 0.0
        nouvelle_route.ajouter_vehicule(self)
        
        return True

    def ajuster_vitesse(self, vehicule_devant: Optional['Vehicule'],
                        distance_securite: float = 0.05) -> None:

        if vehicule_devant is None:
            v_devant = -1.0
            p_devant = -1.0
        else:
            v_devant = vehicule_devant.vitesse
            p_devant = vehicule_devant.position

        self.vitesse = calculer_nouvelle_vitesse(
            self.vitesse,
            self.position,
            self.route_actuelle.limite_vitesse,
            self.vitesse_max,
            v_devant,
            p_devant
        )
    
    def est_arrive(self) -> bool:
        """
        Vérifie si le véhicule a atteint la fin de sa route.
        
        Returns:
            True si le véhicule est arrivé à destination
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
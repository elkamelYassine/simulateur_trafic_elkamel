"""
Module définissant la classe Route pour la simulation de trafic.
"""
from typing import List, Optional
from simulateur_trafic.core.exceptions.exceptions import ErreurReseau

class Route:
    """
    Représente une route dans le réseau routier.
    """
    
    def __init__(self, nom: str, longueur: float, limite_vitesse: float = 90.0,
                 nombre_voies: int = 2):
        """
        Initialise une nouvelle route.
        
        Args:
            nom: Nom identifiant la route
            longueur: Longueur de la route en kilomètres
            limite_vitesse: Vitesse maximale autorisée en km/h
            nombre_voies: Nombre de voies de circulation
        """
        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.nombre_voies = nombre_voies
        self.vehicules: List = []  # Liste des véhicules présents sur la route
        self.routes_suivantes: List['Route'] = []  # Routes accessibles depuis cette route

    def ajouter_vehicule(self, vehicule) -> bool:
        """
        Ajoute un véhicule sur la route.

        Args:
            vehicule: Le véhicule à ajouter

        Returns:
            True si l'ajout a réussi, False sinon
        """
        try:

            if hasattr(self, "capacite_max") and len(self.vehicules) >= self.capacite_max:
                raise ValueError("La route est pleine, impossible d'ajouter un autre véhicule.")

            if vehicule in self.vehicules:
                raise ValueError("Le véhicule est déjà présent sur la route.")

            self.vehicules.append(vehicule)
            vehicule.route_actuelle = self
            return True

        except ValueError as e:
            print(f"Erreur lors de l’ajout du véhicule : {e}")
            return False

    def retirer_vehicule(self, vehicule) -> bool:
        """
        Retire un véhicule de la route.
        
        Args:
            vehicule: Le véhicule à retirer
            
        Returns:
            True si le retrait a réussi, False sinon
        """
        if vehicule in self.vehicules:
            self.vehicules.remove(vehicule)
            return True
        return False
    
    def mettre_a_jour_vehicules(self, delta_t: float) -> None:
        """
        Met à jour la position et la vitesse de tous les véhicules.
        
        Args:
            delta_t: Intervalle de temps en minutes
        """
        # Trier les véhicules par position (du plus avancé au moins avancé)
        self.vehicules.sort(key=lambda v: v.position, reverse=True)
        
        # Mettre à jour chaque véhicule
        for i, vehicule in enumerate(self.vehicules):
            # Trouver le véhicule devant (s'il existe)
            vehicule_devant = self.vehicules[i - 1] if i > 0 else None
            
            # Ajuster la vitesse en fonction du trafic
            vehicule.ajuster_vitesse(vehicule_devant)
            
            # Faire avancer le véhicule
            vehicule.avancer(delta_t)
    
    def retirer_vehicules_arrives(self) -> List:
        """
        Retire les véhicules qui ont atteint la fin de la route.
        
        Returns:
            Liste des véhicules arrivés
        """
        vehicules_arrives = [v for v in self.vehicules if v.est_arrive()]
        
        for vehicule in vehicules_arrives:
            self.retirer_vehicule(vehicule)
        
        return vehicules_arrives

    def connecter_routes(self, nom_route1: str, nom_route2: str) -> bool:
        """
        Connecte deux routes (crée une intersection).

        Args:
            nom_route1: Nom de la première route
            nom_route2: Nom de la route suivante

        Returns:
            True si la connexion a réussi, False sinon
        """
        route1 = self.obtenir_route(nom_route1)
        route2 = self.obtenir_route(nom_route2)

        if not route1:
            raise ErreurReseau(f"Route de départ '{nom_route1}' non trouvée.")
        if not route2:
            raise ErreurReseau(f"Route d'arrivée '{nom_route2}' non trouvée.")

        route1.connecter_route(route2)
        return True

    def connecter_route_suivante(self, route_suivante) -> None:
        """
        Ajoute une route à la liste des routes suivantes possibles.

        Args:
            route_suivante: La Route suivante à connecter
        """
        if route_suivante not in self.routes_suivantes:
            self.routes_suivantes.append(route_suivante)

    def obtenir_densite(self) -> float:
        """
        Calcule la densité de véhicules sur la route.
        
        Returns:
            Nombre de véhicules par kilomètre
        """
        if self.longueur == 0:
            return 0.0
        return len(self.vehicules) / self.longueur
    
    def obtenir_vitesse_moyenne(self) -> float:
        """
        Calcule la vitesse moyenne des véhicules sur la route.
        
        Returns:
            Vitesse moyenne en km/h, 0 si aucun véhicule
        """
        if not self.vehicules:
            return 0.0
        return sum(v.vitesse for v in self.vehicules) / len(self.vehicules)
    
    def est_congestionne(self, seuil_densite: float = 20.0) -> bool:
        """
        Détermine si la route est congestionnée.
        
        Args:
            seuil_densite: Seuil de densité pour considérer une congestion (véhicules/km)
            
        Returns:
            True si la route est congestionnée
        """
        return self.obtenir_densite() > seuil_densite
    
    def obtenir_capacite_restante(self, capacite_max_par_voie: int = 30) -> int:
        """
        Calcule le nombre de véhicules supplémentaires que la route peut accueillir.
        
        Args:
            capacite_max_par_voie: Capacité maximale par voie
            
        Returns:
            Nombre de places disponibles
        """
        capacite_totale = int(self.longueur * self.nombre_voies * capacite_max_par_voie)
        return max(0, capacite_totale - len(self.vehicules))
    
    def __repr__(self) -> str:
        return (f"Route({self.nom}, {self.longueur}km, "
                f"{self.limite_vitesse}km/h, {len(self.vehicules)} véhicules)")
    
    def __str__(self) -> str:
        return (f"{self.nom} [{self.longueur}km, max {self.limite_vitesse}km/h] : "
                f"{len(self.vehicules)} véhicules, "
                f"densité: {self.obtenir_densite():.1f} véh/km, "
                f"vitesse moy: {self.obtenir_vitesse_moyenne():.1f} km/h")
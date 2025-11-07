
from typing import List, Dict, Optional
import random


class ReseauRoutier:
    """
    Représente l'ensemble du réseau routier avec toutes les routes et véhicules.
    """
    
    def __init__(self, nom: str = "Réseau Principal"):
        """
        Initialise un nouveau réseau routier.
        
        Args:
            nom: Nom du réseau
        """
        self.nom = nom
        self.routes: Dict[str, 'Route'] = {}  # Dictionnaire nom -> Route
        self.vehicules: List = []  # Tous les véhicules du réseau
        self.temps_ecoule = 0.0  # Temps total écoulé en minutes
        
    def ajouter_route(self, route) -> None:
        """
        Ajoute une route au réseau.
        
        Args:
            route: La route à ajouter
        """
        if route.nom not in self.routes:
            self.routes[route.nom] = route
    
    def retirer_route(self, nom_route: str) -> bool:
        """
        Retire une route du réseau.
        
        Args:
            nom_route: Nom de la route à retirer
            
        Returns:
            True si le retrait a réussi, False sinon
        """
        if nom_route in self.routes:
            route = self.routes[nom_route]
            # Retirer tous les véhicules de cette route
            for vehicule in route.vehicules[:]:
                self.retirer_vehicule(vehicule)
            del self.routes[nom_route]
            return True
        return False
    
    def obtenir_route(self, nom_route: str):
        """
        Récupère une route par son nom.
        
        Args:
            nom_route: Nom de la route
            
        Returns:
            La route correspondante ou None
        """
        return self.routes.get(nom_route)
    
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

        if route1 and route2:
            route1.connecter_route_suivante(route2)
            return True
        return False
    def ajouter_vehicule(self, vehicule, nom_route: Optional[str] = None) -> bool:
        """
        Ajoute un véhicule au réseau.
        
        Args:
            vehicule: Le véhicule à ajouter
            nom_route: Nom de la route de départ (optionnel)
            
        Returns:
            True si l'ajout a réussi, False sinon
        """
        if vehicule in self.vehicules:
            return False
        
        self.vehicules.append(vehicule)
        
        # Placer le véhicule sur une route si spécifiée
        if nom_route:
            route = self.obtenir_route(nom_route)
            if route:
                route.ajouter_vehicule(vehicule)
                vehicule.route_actuelle = route
        
        return True
    
    def retirer_vehicule(self, vehicule) -> bool:
        """
        Retire un véhicule du réseau.
        
        Args:
            vehicule: Le véhicule à retirer
            
        Returns:
            True si le retrait a réussi, False sinon
        """
        if vehicule in self.vehicules:
            # Retirer de la route actuelle
            if vehicule.route_actuelle:
                vehicule.route_actuelle.retirer_vehicule(vehicule)
            
            self.vehicules.remove(vehicule)
            return True
        return False
    
    def mettre_a_jour(self, delta_t: float) -> None:
        """
        Met à jour l'état de tout le réseau pour un pas de temps.
        
        Args:
            delta_t: Intervalle de temps en minutes
        """
        # Mettre à jour toutes les routes
        for route in self.routes.values():
            route.mettre_a_jour_vehicules(delta_t)
        
        # Gérer les véhicules arrivés à la fin des routes
        self._gerer_transitions_vehicules()
        
        # Incrémenter le temps écoulé
        self.temps_ecoule += delta_t
    
    def _gerer_transitions_vehicules(self) -> None:
        """
        Gère les véhicules qui ont atteint la fin de leur route.
        Ils peuvent soit changer de route, soit quitter le réseau.
        """
        for route in self.routes.values():
            vehicules_arrives = route.retirer_vehicules_arrives()
            
            for vehicule in vehicules_arrives:
                # Si la route a des routes suivantes, choisir une au hasard
                if route.routes_suivantes:
                    nouvelle_route = random.choice(route.routes_suivantes)
                    vehicule.changer_de_route(nouvelle_route)
                else:
                    # Sinon, retirer le véhicule du réseau
                    self.retirer_vehicule(vehicule)
    
    def obtenir_nombre_vehicules(self) -> int:
        """
        Retourne le nombre total de véhicules dans le réseau.
        """
        return len(self.vehicules)
    
    def obtenir_vitesse_moyenne_reseau(self) -> float:
        """
        Calcule la vitesse moyenne de tous les véhicules du réseau.
        
        Returns:
            Vitesse moyenne en km/h
        """
        vehicules_actifs = [v for v in self.vehicules if v.route_actuelle]
        if not vehicules_actifs:
            return 0.0
        return sum(v.vitesse for v in vehicules_actifs) / len(vehicules_actifs)
    
    def obtenir_routes_congestionnees(self, seuil_densite: float = 20.0) -> List:
        """
        Retourne la liste des routes congestionnées.
        
        Args:
            seuil_densite: Seuil de densité pour la congestion
            
        Returns:
            Liste des routes congestionnées
        """
        return [route for route in self.routes.values() 
                if route.est_congestionne(seuil_densite)]
    
    def obtenir_statistiques(self) -> Dict:
        """
        Génère des statistiques globales sur le réseau.
        
        Returns:
            Dictionnaire contenant les statistiques
        """
        routes_congestionnees = self.obtenir_routes_congestionnees()
        
        stats = {
            "temps_ecoule": self.temps_ecoule,
            "nombre_routes": len(self.routes),
            "nombre_vehicules": self.obtenir_nombre_vehicules(),
            "vitesse_moyenne": self.obtenir_vitesse_moyenne_reseau(),
            "routes_congestionnees": len(routes_congestionnees),
            "taux_congestion": (len(routes_congestionnees) / len(self.routes) * 100 
                               if self.routes else 0),
        }
        
        # Statistiques par route
        stats["details_routes"] = {}
        for nom, route in self.routes.items():
            stats["details_routes"][nom] = {
                "nombre_vehicules": len(route.vehicules),
                "densite": route.obtenir_densite(),
                "vitesse_moyenne": route.obtenir_vitesse_moyenne(),
                "congestionne": route.est_congestionne()
            }
        
        return stats
    
    def reinitialiser(self) -> None:
        """
        Réinitialise le réseau (retire tous les véhicules).
        """
        for vehicule in self.vehicules[:]:
            self.retirer_vehicule(vehicule)
        
        self.temps_ecoule = 0.0
    
    def __repr__(self) -> str:
        return (f"ReseauRoutier({self.nom}, {len(self.routes)} routes, "
                f"{self.obtenir_nombre_vehicules()} véhicules)")
    
    def __str__(self) -> str:
        return (f"{self.nom}:\n"
                f"  - {len(self.routes)} routes\n"
                f"  - {self.obtenir_nombre_vehicules()} véhicules\n"
                f"  - Vitesse moyenne: {self.obtenir_vitesse_moyenne_reseau():.1f} km/h\n"
                f"  - Temps écoulé: {self.temps_ecoule:.0f} minutes")
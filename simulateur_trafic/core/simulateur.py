"""
Module définissant la classe Simulateur pour gérer la simulation de trafic.
"""
import json
import random
from typing import Dict, List, Optional, Callable
from pathlib import Path

# Imports relatifs (à adapter selon la structure)
import sys
sys.path.append(str(Path(__file__).parent.parent))

from simulateur_trafic.models.vehicule import Vehicule
from simulateur_trafic.models.route import Route
from simulateur_trafic.models.reseau import ReseauRoutier
from simulateur_trafic.core.exceptions.exceptions import ErreurReseau,ErreurConfiguration

class Simulateur:
    """
    Classe principale pour gérer la simulation du trafic routier.
    """
    
    def __init__(self, fichier_config: Optional[str] = None, reseau: Optional[ReseauRoutier] = None):
        """
        Initialise le simulateur.
        
        Args:
            fichier_config: Chemin vers le fichier de configuration JSON
            reseau: Réseau routier existant (optionnel)
        """
        self.reseau = reseau if reseau else ReseauRoutier()
        self.historique_stats: List[Dict] = []
        self.callbacks: List[Callable] = []  # Fonctions appelées à chaque tour
        self.configuration = {}
        
        if fichier_config:
            self.charger_configuration(fichier_config)

    def charger_configuration(self, fichier_config: str) -> None:
        """
        Charge la configuration du réseau depuis un fichier JSON.

        Args:
            fichier_config: Chemin vers le fichier JSON
        """
        try:
            with open(fichier_config, 'r', encoding='utf-8') as f:
                self.configuration = json.load(f)

            # Créer les routes
            if "routes" in self.configuration:
                for route_data in self.configuration["routes"]:
                    route = Route(
                        nom=route_data["nom"],
                        longueur=route_data["longueur"],
                        limite_vitesse=route_data.get("limite_vitesse", 90.0),
                        nombre_voies=route_data.get("nombre_voies", 2)
                    )
                    self.reseau.ajouter_route(route)

            # Créer les connexions entre routes
            if "connexions" in self.configuration:
                for connexion in self.configuration["connexions"]:
                    # Utilisation d'une gestion d'erreur plus précise
                    try:
                        self.reseau.connecter_routes(
                            connexion["de"],
                            connexion["vers"]
                        )
                    except ErreurReseau as e:
                        # Relève une erreur de configuration si la connexion échoue
                        raise ErreurConfiguration(fichier_config, str(e))

            # Créer les véhicules initiaux
            if "vehicules_initiaux" in self.configuration:
                self._generer_vehicules_initiaux(
                    self.configuration["vehicules_initiaux"]
                )

            print(f"Configuration chargée: {len(self.reseau.routes)} routes, "
                  f"{self.reseau.obtenir_nombre_vehicules()} véhicules")

        except FileNotFoundError:
            print(f"Erreur: Fichier {fichier_config} introuvable")
        except json.JSONDecodeError:
            print(f"Erreur: Format JSON invalide dans {fichier_config}")
        except Exception as e:
        # Gérer les autres exceptions non prévues
            raise ErreurConfiguration(fichier_config, f"Erreur inattendue: {e}")

    def _generer_vehicules_initiaux(self, config_vehicules: Dict) -> None:
        """
        Génère les véhicules initiaux selon la configuration.
        
        Args:
            config_vehicules: Configuration des véhicules
        """
        nombre = config_vehicules.get("nombre", 10)
        vitesse_min = config_vehicules.get("vitesse_min", 60.0)
        vitesse_max = config_vehicules.get("vitesse_max", 120.0)
        routes_depart = config_vehicules.get("routes", list(self.reseau.routes.keys()))
        
        for _ in range(nombre):
            vitesse_initiale = random.uniform(vitesse_min, vitesse_max)
            vehicule = Vehicule(vitesse_initiale=vitesse_initiale)
            
            # Choisir une route de départ aléatoire
            if routes_depart and self.reseau.routes:
                route_nom = random.choice([r for r in routes_depart if r in self.reseau.routes])
                self.reseau.ajouter_vehicule(vehicule, route_nom)
            else:
                self.reseau.ajouter_vehicule(vehicule)
    
    def ajouter_vehicule_aleatoire(self, routes_possibles: Optional[List[str]] = None) -> Vehicule:
        """
        Ajoute un nouveau véhicule aléatoire dans le réseau.
        
        Args:
            routes_possibles: Liste des routes où placer le véhicule
            
        Returns:
            Le véhicule créé
        """
        vitesse_initiale = random.uniform(60, 120)
        vehicule = Vehicule(vitesse_initiale=vitesse_initiale)
        
        if routes_possibles is None:
            routes_possibles = list(self.reseau.routes.keys())
        
        if routes_possibles and self.reseau.routes:
            route_nom = random.choice(routes_possibles)
            self.reseau.ajouter_vehicule(vehicule, route_nom)
        else:
            self.reseau.ajouter_vehicule(vehicule)
        
        return vehicule
    
    def ajouter_callback(self, fonction: Callable) -> None:
        """
        Ajoute une fonction à appeler à chaque tour de simulation.
        
        Args:
            fonction: Fonction prenant en paramètre (tour, stats)
        """
        self.callbacks.append(fonction)

    def lancer_simulation(self, n_tours: int, delta_t: float = 1.0,
                          taux_arrivee: float = 0.0, afficher_progression: bool = True) -> None:
        """
        Lance la simulation pour un nombre donné de tours.

        Args:
            n_tours: Nombre de tours de simulation
            delta_t: Pas de temps en minutes
            taux_arrivee: Probabilité d'arrivée d'un nouveau véhicule par tour (0.0 à 1.0)
            afficher_progression: Afficher les informations de progression
        """
        try:
            # Vérifier la validité du nombre de tours
            if not isinstance(n_tours, int) or n_tours <= 0:
                raise ValueError(f"Nombre d’itérations invalide : {n_tours}. Il doit être un entier positif.")

            # Tentative de lecture d’un fichier de configuration (si applicable)
            # (Ce bloc illustre la gestion de FileNotFoundError)
            try:
                with open("config_simulation.json", "r") as f:
                    config = f.read()
            except FileNotFoundError:
                print(" ️Fichier de configuration 'config_simulation.json' introuvable. Utilisation des valeurs par défaut.")
                config = None

            print(f"\n{'=' * 60}")
            print(f"  DÉBUT DE LA SIMULATION")
            print(f"{'=' * 60}")
            print(f"Paramètres:")
            print(f"  - Nombre de tours: {n_tours}")
            print(f"  - Pas de temps: {delta_t} minute(s)")
            print(f"  - Taux d'arrivée: {taux_arrivee * 100:.1f}%")
            print(f"  - État initial: {self.reseau.obtenir_nombre_vehicules()} véhicules")
            print(f"{'=' * 60}\n")

            # Réinitialiser l'historique
            self.historique_stats = []

            for tour in range(1, n_tours + 1):
                # Ajouter de nouveaux véhicules selon le taux d'arrivée
                if random.random() < taux_arrivee and self.reseau.routes:
                    self.ajouter_vehicule_aleatoire()

                # Mettre à jour le réseau
                self.reseau.mettre_a_jour(delta_t)

                # Collecter les statistiques
                stats = self.reseau.obtenir_statistiques()
                stats["tour"] = tour
                self.historique_stats.append(stats)

                # Appeler les callbacks
                for callback in self.callbacks:
                    callback(tour, stats)

                # Afficher la progression
                if afficher_progression:
                    if tour % max(1, n_tours // 10) == 0 or tour == 1 or tour == n_tours:
                        self._afficher_progression(tour, n_tours, stats)

            print(f"\n{'=' * 60}")
            print(f"  SIMULATION TERMINÉE")
            print(f"{'=' * 60}")
            self._afficher_resume()

        except ValueError as e:
            print(f"Erreur : {e}")
        except FileNotFoundError as e:
            print(f"Erreur de configuration : {e}")
        except Exception as e:
            print(f"Erreur inattendue lors de la simulation : {e}")

    def _afficher_progression(self, tour: int, total_tours: int, stats: Dict) -> None:
        """
        Affiche la progression de la simulation.
        
        Args:
            tour: Numéro du tour actuel
            total_tours: Nombre total de tours
            stats: Statistiques actuelles
        """
        pourcentage = (tour / total_tours) * 100
        nb_vehicules = stats["nombre_vehicules"]
        vitesse_moy = stats["vitesse_moyenne"]
        taux_congestion = stats["taux_congestion"]
        
        print(f"[Tour {tour:4d}/{total_tours}] ({pourcentage:5.1f}%) | "
              f"Véhicules: {nb_vehicules:3d} | "
              f"Vitesse moy: {vitesse_moy:5.1f} km/h | "
              f"Congestion: {taux_congestion:5.1f}%")
    
    def _afficher_resume(self) -> None:
        """
        Affiche un résumé de la simulation.
        """
        if not self.historique_stats:
            print("Aucune donnée de simulation disponible.")
            return
        
        # Calculer les moyennes
        nb_vehicules_moy = sum(s["nombre_vehicules"] for s in self.historique_stats) / len(self.historique_stats)
        vitesse_moy = sum(s["vitesse_moyenne"] for s in self.historique_stats) / len(self.historique_stats)
        congestion_moy = sum(s["taux_congestion"] for s in self.historique_stats) / len(self.historique_stats)
        
        # Trouver les pics
        pic_vehicules = max(self.historique_stats, key=lambda s: s["nombre_vehicules"])
        pic_congestion = max(self.historique_stats, key=lambda s: s["taux_congestion"])
        
        print(f"\n📊 RÉSUMÉ DE LA SIMULATION")
        print(f"{'='*60}")
        print(f"Durée totale simulée: {self.reseau.temps_ecoule:.0f} minutes")
        print(f"\nMoyennes:")
        print(f"  - Véhicules: {nb_vehicules_moy:.1f}")
        print(f"  - Vitesse: {vitesse_moy:.1f} km/h")
        print(f"  - Taux de congestion: {congestion_moy:.1f}%")
        print(f"\nPics:")
        print(f"  - Max véhicules: {pic_vehicules['nombre_vehicules']} (tour {pic_vehicules['tour']})")
        print(f"  - Max congestion: {pic_congestion['taux_congestion']:.1f}% (tour {pic_congestion['tour']})")
        print(f"\nÉtat final du réseau:")
        print(f"  - Véhicules actifs: {self.reseau.obtenir_nombre_vehicules()}")
        print(f"  - Routes congestionnées: {self.historique_stats[-1]['routes_congestionnees']}/{len(self.reseau.routes)}")
    
    def obtenir_historique(self) -> List[Dict]:
        """
        Retourne l'historique complet des statistiques.
        
        Returns:
            Liste des statistiques par tour
        """
        return self.historique_stats
    
    def reinitialiser(self) -> None:
        """
        Réinitialise la simulation.
        """
        self.reseau.reinitialiser()
        self.historique_stats = []
        print("Simulation réinitialisée.")
    
    def sauvegarder_configuration(self, fichier_sortie: str) -> None:
        """
        Sauvegarde la configuration actuelle du réseau.
        
        Args:
            fichier_sortie: Chemin du fichier de sortie
        """
        config = {
            "routes": [],
            "connexions": [],
            "vehicules_initiaux": {
                "nombre": self.reseau.obtenir_nombre_vehicules()
            }
        }
        
        # Sauvegarder les routes
        for nom, route in self.reseau.routes.items():
            config["routes"].append({
                "nom": nom,
                "longueur": route.longueur,
                "limite_vitesse": route.limite_vitesse,
                "nombre_voies": route.nombre_voies
            })
            
            # Sauvegarder les connexions
            for route_suivante in route.routes_suivantes:
                config["connexions"].append({
                    "de": nom,
                    "vers": route_suivante.nom
                })
        
        try:
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"Configuration sauvegardée dans {fichier_sortie}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
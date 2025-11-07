"""
Module définissant la classe Analyseur pour analyser les résultats de simulation.
"""
from typing import Dict, List, Tuple, Optional
import statistics


class Analyseur:
    """
    Analyse les données de simulation et génère des rapports statistiques.
    """
    
    def __init__(self, historique_stats: List[Dict]):
        """
        Initialise l'analyseur avec l'historique des statistiques.
        
        Args:
            historique_stats: Liste des statistiques collectées pendant la simulation
        """
        self.historique = historique_stats
    
    def calculer_vitesse_moyenne_globale(self) -> float:
        """
        Calcule la vitesse moyenne sur toute la simulation.
        
        Returns:
            Vitesse moyenne en km/h
        """
        if not self.historique:
            return 0.0
        
        vitesses = [s["vitesse_moyenne"] for s in self.historique if s["vitesse_moyenne"] > 0]
        return statistics.mean(vitesses) if vitesses else 0.0
    
    def calculer_vitesse_mediane(self) -> float:
        """
        Calcule la vitesse médiane sur toute la simulation.
        
        Returns:
            Vitesse médiane en km/h
        """
        if not self.historique:
            return 0.0
        
        vitesses = [s["vitesse_moyenne"] for s in self.historique if s["vitesse_moyenne"] > 0]
        return statistics.median(vitesses) if vitesses else 0.0
    
    def calculer_ecart_type_vitesse(self) -> float:
        """
        Calcule l'écart-type des vitesses.
        
        Returns:
            Écart-type en km/h
        """
        if not self.historique or len(self.historique) < 2:
            return 0.0
        
        vitesses = [s["vitesse_moyenne"] for s in self.historique if s["vitesse_moyenne"] > 0]
        return statistics.stdev(vitesses) if len(vitesses) >= 2 else 0.0
    
    def identifier_zones_congestion(self, seuil_tours: int = 5) -> Dict[str, int]:
        """
        Identifie les routes fréquemment congestionnées.
        
        Args:
            seuil_tours: Nombre minimum de tours congestionnés pour considérer une route
            
        Returns:
            Dictionnaire {nom_route: nombre_tours_congestionnés}
        """
        congestion_count: Dict[str, int] = {}
        
        for stats in self.historique:
            if "details_routes" in stats:
                for nom_route, details in stats["details_routes"].items():
                    if details.get("congestionne", False):
                        congestion_count[nom_route] = congestion_count.get(nom_route, 0) + 1
        
        # Filtrer selon le seuil
        return {route: count for route, count in congestion_count.items() if count >= seuil_tours}
    
    def calculer_temps_parcours_moyen(self) -> Dict[str, float]:
        """
        Calcule le temps de parcours moyen par route.
        
        Returns:
            Dictionnaire {nom_route: temps_moyen_minutes}
        """
        temps_par_route: Dict[str, List[float]] = {}
        
        for stats in self.historique:
            if "details_routes" in stats:
                for nom_route, details in stats["details_routes"].items():
                    vitesse_moy = details.get("vitesse_moyenne", 0)
                    if vitesse_moy > 0:
                        # Estimer le temps basé sur la vitesse moyenne
                        # (nécessiterait les données de longueur de route)
                        if nom_route not in temps_par_route:
                            temps_par_route[nom_route] = []
        
        return {route: statistics.mean(temps) if temps else 0 
                for route, temps in temps_par_route.items()}
    
    def analyser_densite_trafic(self) -> Dict[str, Dict[str, float]]:
        """
        Analyse la densité du trafic par route.
        
        Returns:
            Dictionnaire avec statistiques de densité par route
        """
        densites_par_route: Dict[str, List[float]] = {}
        
        for stats in self.historique:
            if "details_routes" in stats:
                for nom_route, details in stats["details_routes"].items():
                    densite = details.get("densite", 0)
                    if nom_route not in densites_par_route:
                        densites_par_route[nom_route] = []
                    densites_par_route[nom_route].append(densite)
        
        resultats = {}
        for route, densites in densites_par_route.items():
            if densites:
                resultats[route] = {
                    "moyenne": statistics.mean(densites),
                    "mediane": statistics.median(densites),
                    "min": min(densites),
                    "max": max(densites),
                    "ecart_type": statistics.stdev(densites) if len(densites) >= 2 else 0
                }
        
        return resultats
    
    def detecter_heures_pointe(self, fenetre: int = 5) -> List[Tuple[int, float]]:
        """
        Détecte les périodes de forte congestion (heures de pointe).
        
        Args:
            fenetre: Taille de la fenêtre glissante en tours
            
        Returns:
            Liste de tuples (tour, taux_congestion_moyen)
        """
        if len(self.historique) < fenetre:
            return []
        
        heures_pointe = []
        
        for i in range(len(self.historique) - fenetre + 1):
            fenetre_stats = self.historique[i:i + fenetre]
            taux_moyen = statistics.mean([s["taux_congestion"] for s in fenetre_stats])
            
            # Considérer comme heure de pointe si > 50%
            if taux_moyen > 50:
                tour_central = i + fenetre // 2
                heures_pointe.append((tour_central, taux_moyen))
        
        return heures_pointe
    
    def calculer_efficacite_reseau(self) -> float:
        """
        Calcule un score d'efficacité du réseau (0-100).
        Basé sur la vitesse moyenne et le taux de congestion.
        
        Returns:
            Score d'efficacité (0-100)
        """
        if not self.historique:
            return 0.0
        
        # Vitesse moyenne normalisée (supposons vitesse max = 120 km/h)
        vitesse_moy = self.calculer_vitesse_moyenne_globale()
        score_vitesse = (vitesse_moy / 120.0) * 50  # Max 50 points
        
        # Inverse du taux de congestion
        taux_congestion_moy = statistics.mean([s["taux_congestion"] for s in self.historique])
        score_fluidite = (100 - taux_congestion_moy) / 2  # Max 50 points
        
        return min(100, score_vitesse + score_fluidite)
    
    def generer_rapport_complet(self) -> Dict:
        """
        Génère un rapport complet d'analyse.
        
        Returns:
            Dictionnaire contenant toutes les analyses
        """
        if not self.historique:
            return {"erreur": "Aucune donnée à analyser"}
        
        rapport = {
            "resume_general": {
                "nombre_tours": len(self.historique),
                "duree_totale": self.historique[-1].get("temps_ecoule", 0),
                "vitesse_moyenne": self.calculer_vitesse_moyenne_globale(),
                "vitesse_mediane": self.calculer_vitesse_mediane(),
                "ecart_type_vitesse": self.calculer_ecart_type_vitesse(),
                "efficacite_reseau": self.calculer_efficacite_reseau()
            },
            "congestion": {
                "zones_congestionnees": self.identifier_zones_congestion(),
                "heures_pointe": self.detecter_heures_pointe(),
                "taux_moyen": statistics.mean([s["taux_congestion"] for s in self.historique])
            },
            "densite_trafic": self.analyser_densite_trafic(),
            "evolution_vehicules": {
                "initial": self.historique[0]["nombre_vehicules"],
                "final": self.historique[-1]["nombre_vehicules"],
                "maximum": max(s["nombre_vehicules"] for s in self.historique),
                "minimum": min(s["nombre_vehicules"] for s in self.historique),
                "moyenne": statistics.mean([s["nombre_vehicules"] for s in self.historique])
            }
        }
        
        return rapport
    
    def comparer_routes(self) -> List[Tuple[str, Dict]]:
        """
        Compare les performances de toutes les routes.
        
        Returns:
            Liste de tuples (nom_route, statistiques) triée par performance
        """
        performances: Dict[str, Dict] = {}
        
        # Collecter les données par route
        for stats in self.historique:
            if "details_routes" in stats:
                for nom_route, details in stats["details_routes"].items():
                    if nom_route not in performances:
                        performances[nom_route] = {
                            "vitesses": [],
                            "densites": [],
                            "nb_vehicules": [],
                            "tours_congestion": 0
                        }
                    
                    performances[nom_route]["vitesses"].append(details.get("vitesse_moyenne", 0))
                    performances[nom_route]["densites"].append(details.get("densite", 0))
                    performances[nom_route]["nb_vehicules"].append(details.get("nombre_vehicules", 0))
                    
                    if details.get("congestionne", False):
                        performances[nom_route]["tours_congestion"] += 1
        
        # Calculer les moyennes et scores
        resultats = []
        for route, data in performances.items():
            vitesse_moy = statistics.mean(data["vitesses"]) if data["vitesses"] else 0
            densite_moy = statistics.mean(data["densites"]) if data["densites"] else 0
            taux_congestion = (data["tours_congestion"] / len(self.historique)) * 100
            
            # Score de performance (vitesse haute = bon, congestion basse = bon)
            score = vitesse_moy - (taux_congestion * 0.5)
            
            resultats.append((route, {
                "vitesse_moyenne": vitesse_moy,
                "densite_moyenne": densite_moy,
                "taux_congestion": taux_congestion,
                "score_performance": score
            }))
        
        # Trier par score décroissant
        resultats.sort(key=lambda x: x[1]["score_performance"], reverse=True)
        
        return resultats
    
    def afficher_rapport_console(self) -> None:
        """
        Affiche un rapport formaté dans la console.
        """
        rapport = self.generer_rapport_complet()
        
        print("\n" + "="*70)
        print(" "*20 + "📊 RAPPORT D'ANALYSE 📊")
        print("="*70)
        
        # Résumé général
        print("\n🔍 RÉSUMÉ GÉNÉRAL")
        print("-" * 70)
        resume = rapport["resume_general"]
        print(f"Nombre de tours simulés: {resume['nombre_tours']}")
        print(f"Durée totale: {resume['duree_totale']:.0f} minutes")
        print(f"Vitesse moyenne: {resume['vitesse_moyenne']:.2f} km/h")
        print(f"Vitesse médiane: {resume['vitesse_mediane']:.2f} km/h")
        print(f"Écart-type vitesse: {resume['ecart_type_vitesse']:.2f} km/h")
        print(f"Score d'efficacité: {resume['efficacite_reseau']:.1f}/100")
        
        # Congestion
        print("\n🚦 ANALYSE DE CONGESTION")
        print("-" * 70)
        congestion = rapport["congestion"]
        print(f"Taux de congestion moyen: {congestion['taux_moyen']:.2f}%")
        
        if congestion["zones_congestionnees"]:
            print("\nRoutes fréquemment congestionnées:")
            for route, count in sorted(congestion["zones_congestionnees"].items(), 
                                       key=lambda x: x[1], reverse=True):
                print(f"  • {route}: {count} tours ({count/resume['nombre_tours']*100:.1f}%)")
        else:
            print("Aucune zone de congestion détectée.")
        
        if congestion["heures_pointe"]:
            print(f"\nHeures de pointe détectées: {len(congestion['heures_pointe'])} périodes")
        
        # Évolution des véhicules
        print("\n🚗 ÉVOLUTION DES VÉHICULES")
        print("-" * 70)
        evol = rapport["evolution_vehicules"]
        print(f"Initial: {evol['initial']} | Final: {evol['final']}")
        print(f"Maximum: {evol['maximum']} | Minimum: {evol['minimum']}")
        print(f"Moyenne: {evol['moyenne']:.1f}")
        
        # Comparaison des routes
        print("\n🛣️  COMPARAISON DES ROUTES")
        print("-" * 70)
        comparaison = self.comparer_routes()
        for i, (route, stats) in enumerate(comparaison[:5], 1):  # Top 5
            print(f"{i}. {route}")
            print(f"   Vitesse moy: {stats['vitesse_moyenne']:.1f} km/h | "
                  f"Densité: {stats['densite_moyenne']:.1f} véh/km | "
                  f"Congestion: {stats['taux_congestion']:.1f}%")
        
        print("\n" + "="*70 + "\n")
"""
Module pour l'affichage graphique des résultats de simulation.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Dict, Optional
import numpy as np


class AffichageGraphique:
    """
    Gère l'affichage graphique des résultats de simulation.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialise le système d'affichage.
        
        Args:
            style: Style matplotlib à utiliser
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        self.fig = None
        self.axes = None
    
    def tracer_evolution_vehicules(self, historique: List[Dict], 
                                   sauvegarder: Optional[str] = None) -> None:
        """
        Trace l'évolution du nombre de véhicules au cours du temps.
        
        Args:
            historique: Liste des statistiques de simulation
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        if not historique:
            print("Aucune donnée à afficher")
            return
        
        tours = [s["tour"] for s in historique]
        nb_vehicules = [s["nombre_vehicules"] for s in historique]
        
        plt.figure(figsize=(12, 6))
        plt.plot(tours, nb_vehicules, linewidth=2, color='#2E86AB', marker='o', 
                markersize=3, markevery=max(1, len(tours)//20))
        plt.xlabel('Tour de simulation', fontsize=12, fontweight='bold')
        plt.ylabel('Nombre de véhicules', fontsize=12, fontweight='bold')
        plt.title('Évolution du nombre de véhicules dans le réseau', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé: {sauvegarder}")
        
        plt.show()
    
    def tracer_vitesse_moyenne(self, historique: List[Dict], 
                              sauvegarder: Optional[str] = None) -> None:
        """
        Trace l'évolution de la vitesse moyenne.
        
        Args:
            historique: Liste des statistiques de simulation
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        if not historique:
            print("Aucune donnée à afficher")
            return
        
        tours = [s["tour"] for s in historique]
        vitesses = [s["vitesse_moyenne"] for s in historique]
        
        plt.figure(figsize=(12, 6))
        plt.plot(tours, vitesses, linewidth=2, color='#A23B72', marker='s', 
                markersize=3, markevery=max(1, len(tours)//20))
        plt.axhline(y=np.mean(vitesses), color='red', linestyle='--', 
                   linewidth=2, label=f'Moyenne: {np.mean(vitesses):.1f} km/h')
        plt.xlabel('Tour de simulation', fontsize=12, fontweight='bold')
        plt.ylabel('Vitesse moyenne (km/h)', fontsize=12, fontweight='bold')
        plt.title('Évolution de la vitesse moyenne dans le réseau', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé: {sauvegarder}")
        
        plt.show()
    
    def tracer_taux_congestion(self, historique: List[Dict], 
                              seuil: float = 50.0,
                              sauvegarder: Optional[str] = None) -> None:
        """
        Trace l'évolution du taux de congestion.
        
        Args:
            historique: Liste des statistiques de simulation
            seuil: Seuil de congestion critique (en %)
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        if not historique:
            print("Aucune donnée à afficher")
            return
        
        tours = [s["tour"] for s in historique]
        taux = [s["taux_congestion"] for s in historique]
        
        plt.figure(figsize=(12, 6))
        
        # Colorer les zones selon le niveau de congestion
        plt.fill_between(tours, 0, taux, where=[t < seuil for t in taux], 
                        color='green', alpha=0.3, label='Fluide')
        plt.fill_between(tours, 0, taux, where=[t >= seuil for t in taux], 
                        color='red', alpha=0.3, label='Congestionné')
        
        plt.plot(tours, taux, linewidth=2, color='#F18F01', marker='D', 
                markersize=3, markevery=max(1, len(tours)//20))
        plt.axhline(y=seuil, color='darkred', linestyle='--', linewidth=2, 
                   label=f'Seuil critique: {seuil}%')
        
        plt.xlabel('Tour de simulation', fontsize=12, fontweight='bold')
        plt.ylabel('Taux de congestion (%)', fontsize=12, fontweight='bold')
        plt.title('Évolution du taux de congestion', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé: {sauvegarder}")
        
        plt.show()
    
    def tracer_dashboard_complet(self, historique: List[Dict], 
                                sauvegarder: Optional[str] = None) -> None:
        """
        Crée un dashboard complet avec plusieurs graphiques.
        
        Args:
            historique: Liste des statistiques de simulation
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        if not historique:
            print("Aucune donnée à afficher")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dashboard de Simulation du Trafic Routier', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        tours = [s["tour"] for s in historique]
        
        # 1. Nombre de véhicules
        ax1 = axes[0, 0]
        nb_vehicules = [s["nombre_vehicules"] for s in historique]
        ax1.plot(tours, nb_vehicules, linewidth=2, color='#2E86AB')
        ax1.fill_between(tours, nb_vehicules, alpha=0.3, color='#2E86AB')
        ax1.set_xlabel('Tour', fontweight='bold')
        ax1.set_ylabel('Nombre de véhicules', fontweight='bold')
        ax1.set_title('Évolution du nombre de véhicules', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # 2. Vitesse moyenne
        ax2 = axes[0, 1]
        vitesses = [s["vitesse_moyenne"] for s in historique]
        ax2.plot(tours, vitesses, linewidth=2, color='#A23B72')
        ax2.axhline(y=np.mean(vitesses), color='red', linestyle='--', 
                   label=f'Moy: {np.mean(vitesses):.1f} km/h')
        ax2.set_xlabel('Tour', fontweight='bold')
        ax2.set_ylabel('Vitesse (km/h)', fontweight='bold')
        ax2.set_title('Vitesse moyenne', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Taux de congestion
        ax3 = axes[1, 0]
        taux = [s["taux_congestion"] for s in historique]
        ax3.fill_between(tours, taux, alpha=0.5, color='#F18F01')
        ax3.plot(tours, taux, linewidth=2, color='#F18F01')
        ax3.axhline(y=50, color='darkred', linestyle='--', label='Seuil: 50%')
        ax3.set_xlabel('Tour', fontweight='bold')
        ax3.set_ylabel('Taux de congestion (%)', fontweight='bold')
        ax3.set_title('Taux de congestion', fontweight='bold')
        ax3.set_ylim(0, 100)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Statistiques récapitulatives
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        stats_text = f"""
        STATISTIQUES GLOBALES
        {'='*35}
        
        Simulation:
          • Durée: {historique[-1]['temps_ecoule']:.0f} minutes
          • Tours: {len(historique)}
        
        Véhicules:
          • Initial: {historique[0]['nombre_vehicules']}
          • Final: {historique[-1]['nombre_vehicules']}
          • Maximum: {max(nb_vehicules)}
          • Moyenne: {np.mean(nb_vehicules):.1f}
        
        Vitesse:
          • Moyenne: {np.mean(vitesses):.2f} km/h
          • Max: {max(vitesses):.2f} km/h
          • Min: {min(vitesses):.2f} km/h
        
        Congestion:
          • Taux moyen: {np.mean(taux):.2f}%
          • Taux max: {max(taux):.2f}%
        """
        
        ax4.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center')
        
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Dashboard sauvegardé: {sauvegarder}")
        
        plt.show()
    
    def tracer_densite_par_route(self, historique: List[Dict], 
                                 top_n: int = 10,
                                 sauvegarder: Optional[str] = None) -> None:
        """
        Trace un diagramme en barres de la densité moyenne par route.
        
        Args:
            historique: Liste des statistiques de simulation
            top_n: Nombre de routes à afficher
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        if not historique:
            print("Aucune donnée à afficher")
            return
        
        # Calculer la densité moyenne par route
        densites_routes = {}
        for stats in historique:
            if "details_routes" in stats:
                for route, details in stats["details_routes"].items():
                    if route not in densites_routes:
                        densites_routes[route] = []
                    densites_routes[route].append(details.get("densite", 0))
        
        # Calculer les moyennes
        moyennes = {route: np.mean(vals) for route, vals in densites_routes.items()}
        
        # Trier et prendre les top_n
        routes_triees = sorted(moyennes.items(), key=lambda x: x[1], reverse=True)[:top_n]
        routes = [r[0] for r in routes_triees]
        valeurs = [r[1] for r in routes_triees]
        
        plt.figure(figsize=(12, 6))
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(routes)))
        bars = plt.barh(routes, valeurs, color=colors, edgecolor='black', linewidth=1.2)
        
        # Ajouter les valeurs sur les barres
        for i, (bar, val) in enumerate(zip(bars, valeurs)):
            plt.text(val, i, f' {val:.1f}', va='center', fontweight='bold')
        
        plt.xlabel('Densité moyenne (véhicules/km)', fontsize=12, fontweight='bold')
        plt.ylabel('Route', fontsize=12, fontweight='bold')
        plt.title(f'Top {len(routes)} - Densité moyenne par route', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Graphique sauvegardé: {sauvegarder}")
        
        plt.show()
    
    def tracer_heatmap_congestion(self, historique: List[Dict],
                                 sauvegarder: Optional[str] = None) -> None:
        """
        Crée une heatmap de la congestion par route au fil du temps.
        
        Args:
            historique: Liste des statistiques de simulation
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        if not historique:
            print("Aucune donnée à afficher")
            return
        
        # Extraire les données
        routes_set = set()
        for stats in historique:
            if "details_routes" in stats:
                routes_set.update(stats["details_routes"].keys())
        
        routes = sorted(list(routes_set))
        tours = [s["tour"] for s in historique]
        
        # Créer la matrice de densité
        matrice = np.zeros((len(routes), len(tours)))
        
        for j, stats in enumerate(historique):
            if "details_routes" in stats:
                for i, route in enumerate(routes):
                    if route in stats["details_routes"]:
                        matrice[i, j] = stats["details_routes"][route].get("densite", 0)
        
        plt.figure(figsize=(14, max(6, len(routes) * 0.4)))
        im = plt.imshow(matrice, aspect='auto', cmap='YlOrRd', interpolation='nearest')
        
        plt.colorbar(im, label='Densité (véhicules/km)')
        plt.xlabel('Tour de simulation', fontsize=12, fontweight='bold')
        plt.ylabel('Route', fontsize=12, fontweight='bold')
        plt.title('Heatmap de la densité du trafic', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Configurer les axes
        plt.yticks(range(len(routes)), routes)
        
        # Afficher les ticks de tours de manière espacée
        n_ticks = min(10, len(tours))
        tick_positions = np.linspace(0, len(tours)-1, n_ticks, dtype=int)
        plt.xticks(tick_positions, [tours[i] for i in tick_positions])
        
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Heatmap sauvegardée: {sauvegarder}")
        
        plt.show()
    
    def visualiser_reseau(self, reseau, sauvegarder: Optional[str] = None) -> None:
        """
        Visualise la structure du réseau routier.
        
        Args:
            reseau: Instance de ReseauRoutier
            sauvegarder: Chemin pour sauvegarder la figure (optionnel)
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Positionner les routes en cercle
        n_routes = len(reseau.routes)
        angles = np.linspace(0, 2*np.pi, n_routes, endpoint=False)
        positions = {}
        
        for i, (nom, route) in enumerate(reseau.routes.items()):
            x = np.cos(angles[i]) * 5
            y = np.sin(angles[i]) * 5
            positions[nom] = (x, y)
            
            # Dessiner la route comme un cercle
            nb_vehicules = len(route.vehicules)
            couleur = plt.cm.Reds(min(nb_vehicules / 20, 1.0))
            
            circle = patches.Circle((x, y), 0.5, color=couleur, 
                                   edgecolor='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            
            # Ajouter le nom et les infos
            ax.text(x, y, nom, ha='center', va='center', 
                   fontsize=8, fontweight='bold', zorder=4)
            ax.text(x, y-0.8, f'{nb_vehicules} véh\n{route.vitesse_moyenne:.0f} km/h', 
                   ha='center', va='top', fontsize=7, zorder=4)
        
        # Dessiner les connexions
        for nom_route, route in reseau.routes.items():
            x1, y1 = positions[nom_route]
            for route_suivante in route.routes_suivantes:
                if route_suivante.nom in positions:
                    x2, y2 = positions[route_suivante.nom]
                    ax.arrow(x1, y1, (x2-x1)*0.85, (y2-y1)*0.85, 
                            head_width=0.2, head_length=0.2, 
                            fc='gray', ec='gray', alpha=0.5, zorder=1)
        
        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Visualisation du réseau routier\n(Intensité de couleur = nombre de véhicules)', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if sauvegarder:
            plt.savefig(sauvegarder, dpi=300, bbox_inches='tight')
            print(f"Visualisation sauvegardée: {sauvegarder}")
        
        plt.show()
"""
Module pour l'export des résultats de simulation dans différents formats.
"""
import json
import csv
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class ExporteurResultats:
    """
    Gère l'export des résultats de simulation dans différents formats.
    """
    
    def __init__(self, dossier_sortie: str = "resultats"):
        """
        Initialise l'exporteur.
        Args:
            dossier_sortie: Dossier où sauvegarder les fichiers
        """
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.dossier_sortie = Path(dossier_sortie) / f"simulation_{self.timestamp}"
        self.dossier_sortie.mkdir(parents=True, exist_ok=True)

    def exporter_json(self, historique: List[Dict], nom_fichier: Optional[str] = None) -> str:
        if nom_fichier is None:
            nom_fichier = f"historique_{self.timestamp}.json"
        chemin = self.dossier_sortie / nom_fichier
        data = {
            "metadata": {
                "date_export": datetime.now().isoformat(),
                "nombre_tours": len(historique),
                "duree_simulation": historique[-1]["temps_ecoule"] if historique else 0
            },
            "historique": historique
        }
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return str(chemin)
        except Exception as e:
            print(f"Erreur export JSON: {e}")
            return ""

    
    
    def exporter_csv_global(self, historique: List[Dict], nom_fichier: Optional[str] = None) -> str:
        """
        Exporte les statistiques globales en format CSV.
        
        Args:
            historique: Liste des statistiques de simulation
            nom_fichier: Nom du fichier (optionnel)
            
        Returns:
            Chemin du fichier créé
        """
        if nom_fichier is None:
            nom_fichier = f"simulation_global_{self.timestamp}.csv"
        
        chemin = self.dossier_sortie / nom_fichier
        
        if not historique:
            print("Aucune donnée à exporter")
            return ""
        
        try:
            with open(chemin, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                
                # En-têtes
                writer.writerow([
                    'Tour',
                    'Temps écoulé (min)',
                    'Nombre véhicules',
                    'Vitesse moyenne (km/h)',
                    'Taux congestion (%)',
                    'Routes congestionnées'
                ])
                
                # Données
                for stats in historique:
                    writer.writerow([
                        stats.get('tour', 0),
                        stats.get('temps_ecoule', 0),
                        stats.get('nombre_vehicules', 0),
                        f"{stats.get('vitesse_moyenne', 0):.2f}",
                        f"{stats.get('taux_congestion', 0):.2f}",
                        stats.get('routes_congestionnees', 0)
                    ])
            
            print(f"✅ Export CSV global réussi: {chemin}")
            return str(chemin)
        except Exception as e:
            print(f"❌ Erreur lors de l'export CSV: {e}")
            return ""
    
    def exporter_csv_par_route(self, historique: List[Dict], nom_fichier: Optional[str] = None) -> str:
        """
        Exporte les statistiques détaillées par route en format CSV.
        
        Args:
            historique: Liste des statistiques de simulation
            nom_fichier: Nom du fichier (optionnel)
            
        Returns:
            Chemin du fichier créé
        """
        if nom_fichier is None:
            nom_fichier = f"simulation_routes_{self.timestamp}.csv"
        
        chemin = self.dossier_sortie / nom_fichier
        
        if not historique:
            print("Aucune donnée à exporter")
            return ""
        
        try:
            with open(chemin, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                
                # En-têtes
                writer.writerow([
                    'Tour',
                    'Route',
                    'Nombre véhicules',
                    'Densité (véh/km)',
                    'Vitesse moyenne (km/h)',
                    'Congestionnée'
                ])
                
                # Données
                for stats in historique:
                    tour = stats.get('tour', 0)
                    if 'details_routes' in stats:
                        for nom_route, details in stats['details_routes'].items():
                            writer.writerow([
                                tour,
                                nom_route,
                                details.get('nombre_vehicules', 0),
                                f"{details.get('densite', 0):.2f}",
                                f"{details.get('vitesse_moyenne', 0):.2f}",
                                'Oui' if details.get('congestionne', False) else 'Non'
                            ])
            
            print(f"✅ Export CSV par route réussi: {chemin}")
            return str(chemin)
        except Exception as e:
            print(f"❌ Erreur lors de l'export CSV: {e}")
            return ""
    
    def exporter_rapport_texte(self, rapport: Dict, nom_fichier: Optional[str] = None) -> str:
        """
        Exporte un rapport d'analyse en format texte.
        
        Args:
            rapport: Dictionnaire contenant le rapport d'analyse
            nom_fichier: Nom du fichier (optionnel)
            
        Returns:
            Chemin du fichier créé
        """
        if nom_fichier is None:
            nom_fichier = f"rapport_analyse_{self.timestamp}.txt"
        
        chemin = self.dossier_sortie / nom_fichier
        
        try:
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(" "*25 + "RAPPORT D'ANALYSE DE SIMULATION\n")
                f.write("="*80 + "\n\n")
                f.write(f"Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Résumé général
                if 'resume_general' in rapport:
                    f.write("RÉSUMÉ GÉNÉRAL\n")
                    f.write("-"*80 + "\n")
                    resume = rapport['resume_general']
                    f.write(f"Nombre de tours simulés: {resume.get('nombre_tours', 0)}\n")
                    f.write(f"Durée totale: {resume.get('duree_totale', 0):.0f} minutes\n")
                    f.write(f"Vitesse moyenne: {resume.get('vitesse_moyenne', 0):.2f} km/h\n")
                    f.write(f"Vitesse médiane: {resume.get('vitesse_mediane', 0):.2f} km/h\n")
                    f.write(f"Écart-type vitesse: {resume.get('ecart_type_vitesse', 0):.2f} km/h\n")
                    f.write(f"Score d'efficacité: {resume.get('efficacite_reseau', 0):.1f}/100\n\n")
                
                # Congestion
                if 'congestion' in rapport:
                    f.write("ANALYSE DE CONGESTION\n")
                    f.write("-"*80 + "\n")
                    congestion = rapport['congestion']
                    f.write(f"Taux de congestion moyen: {congestion.get('taux_moyen', 0):.2f}%\n\n")
                    
                    if congestion.get('zones_congestionnees'):
                        f.write("Routes fréquemment congestionnées:\n")
                        for route, count in sorted(congestion['zones_congestionnees'].items(), 
                                                   key=lambda x: x[1], reverse=True):
                            pourcentage = (count / resume.get('nombre_tours', 1)) * 100
                            f.write(f"  • {route}: {count} tours ({pourcentage:.1f}%)\n")
                    else:
                        f.write("Aucune zone de congestion significative détectée.\n")
                    f.write("\n")
                    
                    if congestion.get('heures_pointe'):
                        f.write(f"Heures de pointe détectées: {len(congestion['heures_pointe'])} périodes\n")
                        for tour, taux in congestion['heures_pointe'][:5]:  # Top 5
                            f.write(f"  • Tour {tour}: {taux:.1f}% de congestion\n")
                        f.write("\n")
                
                # Évolution des véhicules
                if 'evolution_vehicules' in rapport:
                    f.write("ÉVOLUTION DES VÉHICULES\n")
                    f.write("-"*80 + "\n")
                    evol = rapport['evolution_vehicules']
                    f.write(f"Nombre initial: {evol.get('initial', 0)}\n")
                    f.write(f"Nombre final: {evol.get('final', 0)}\n")
                    f.write(f"Maximum: {evol.get('maximum', 0)}\n")
                    f.write(f"Minimum: {evol.get('minimum', 0)}\n")
                    f.write(f"Moyenne: {evol.get('moyenne', 0):.1f}\n\n")
                
                 # Densité du trafic
                if 'densite_trafic' in rapport:
                    f.write("DENSITÉ DU TRAFIC\n")
                    f.write("-"*80 + "\n")
                    densite = rapport['densite_trafic']
                    f.write(f"Densité moyenne: {densite.get('moyenne', 0):.2f} véhicules/km\n")
                    f.write(f"Densité maximale: {densite.get('maximale', 0):.2f} véhicules/km\n")
                    f.write(f"Densité minimale: {densite.get('minimale', 0):.2f} véhicules/km\n\n")
                
                # Statistiques par route
                if 'statistiques_routes' in rapport:
                    f.write("STATISTIQUES PAR ROUTE\n")
                    f.write("-"*80 + "\n")
                    stats_routes = rapport['statistiques_routes']
                    for route, stats in stats_routes.items():
                        f.write(f"Route: {route}\n")
                        f.write(f"  - Vitesse moyenne: {stats.get('vitesse_moyenne', 0):.2f} km/h\n")
                        f.write(f"  - Densité moyenne: {stats.get('densite_moyenne', 0):.2f} véhicules/km\n")
                        f.write(f"  - Taux de congestion: {stats.get('taux_congestion', 0):.2f}%\n")
                        f.write("\n")
                
                # Ajout d'autres sections personnalisées si besoin
                if 'autres' in rapport:
                    f.write("AUTRES INFORMATIONS\n")
                    f.write("-"*80 + "\n")
                    autres = rapport['autres']
                    for cle, valeur in autres.items():
                        f.write(f"{cle}: {valeur}\n")
                    f.write("\n")
            
            print(f"✅ Export rapport texte réussi: {chemin}")
            return str(chemin)
        except Exception as e:
            print(f"❌ Erreur lors de l'export du rapport texte: {e}")
            return ""
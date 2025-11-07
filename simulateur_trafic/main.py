import json
from pathlib import Path
from .inputOutput.export import ExporteurResultats

def charger_config(path_config):
    with open(path_config, "r", encoding="utf-8") as f:
        return json.load(f)

def simuler_trafic(config):
    # Simulation factice pour l'exemple
    historique = []
    for tour in range(1, config["simulation"]["nombre_tours"] + 1):
        stats = {
            "tour": tour,
            "temps_ecoule": tour * config["simulation"]["pas_temps_minutes"],
            "nombre_vehicules": config["vehicules"]["nombre_initial"] + tour * config["vehicules"]["taux_arrivee_par_tour"] - tour * config["vehicules"]["taux_depart_par_tour"],
            "vitesse_moyenne": 40 + (tour % 5),
            "taux_congestion": 10 + (tour % 3) * 2,
            "routes_congestionnees": (tour % len(config["reseau"]["routes"])) + 1,
            "details_routes": {
                route["nom"]: {
                    "nombre_vehicules": 20 + tour,
                    "densite": 10 + tour * 0.5,
                    "vitesse_moyenne": 35 + (tour % 3),
                    "congestionne": (tour % 2 == 0)
                }
                for route in config["reseau"]["routes"]
            }
        }
        historique.append(stats)
    return historique

def analyser_resultats(historique):
    # Analyse factice pour l'exemple
    rapport = {
        "resume_general": {
            "nombre_tours": len(historique),
            "duree_totale": historique[-1]["temps_ecoule"] if historique else 0,
            "vitesse_moyenne": sum(h["vitesse_moyenne"] for h in historique) / len(historique) if historique else 0,
            "vitesse_mediane": sorted([h["vitesse_moyenne"] for h in historique])[len(historique)//2] if historique else 0,
            "ecart_type_vitesse": 2.0,
            "efficacite_reseau": 85.0
        },
        "congestion": {
            "taux_moyen": sum(h["taux_congestion"] for h in historique) / len(historique) if historique else 0,
            "zones_congestionnees": {
                route: sum(1 for h in historique if h["details_routes"][route]["congestionne"])
                for route in historique[0]["details_routes"]
            } if historique else {},
            "heures_pointe": [(h["tour"], h["taux_congestion"]) for h in historique if h["taux_congestion"] > 12]
        },
        "evolution_vehicules": {
            "initial": historique[0]["nombre_vehicules"] if historique else 0,
            "final": historique[-1]["nombre_vehicules"] if historique else 0,
            "maximum": max(h["nombre_vehicules"] for h in historique) if historique else 0,
            "minimum": min(h["nombre_vehicules"] for h in historique) if historique else 0,
            "moyenne": sum(h["nombre_vehicules"] for h in historique) / len(historique) if historique else 0
        },
        "densite_trafic": {
            "moyenne": sum(h["details_routes"][list(h["details_routes"].keys())[0]]["densite"] for h in historique) / len(historique) if historique else 0,
            "maximale": max(h["details_routes"][list(h["details_routes"].keys())[0]]["densite"] for h in historique) if historique else 0,
            "minimale": min(h["details_routes"][list(h["details_routes"].keys())[0]]["densite"] for h in historique) if historique else 0
        },
        "statistiques_routes": {
            route: {
                "vitesse_moyenne": sum(h["details_routes"][route]["vitesse_moyenne"] for h in historique) / len(historique),
                "densite_moyenne": sum(h["details_routes"][route]["densite"] for h in historique) / len(historique),
                "taux_congestion": 100.0 * sum(1 for h in historique if h["details_routes"][route]["congestionne"]) / len(historique)
            }
            for route in historique[0]["details_routes"]
        } if historique else {},
        "autres": {
            "Note": "Simulation générée automatiquement."
        }
    }
    return rapport

def main():
    config_path = Path(__file__).parent / "data" / "config_reseau.json"
    config = charger_config(config_path)
    historique = simuler_trafic(config)
    rapport = analyser_resultats(historique)

    exporteur = ExporteurResultats()
    exporteur.exporter_json(historique)
    exporteur.exporter_csv_global(historique)
    exporteur.exporter_csv_par_route(historique)
    exporteur.exporter_rapport_texte(rapport)

if __name__ == "__main__":
    main()
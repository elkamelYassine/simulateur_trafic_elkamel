import pytest
import json
import tempfile
from pathlib import Path
from simulateur_trafic.main import charger_config, simuler_trafic, analyser_resultats


class TestSimulateur:
    """Tests pour l'intégration du simulateur complet."""

    @pytest.fixture
    def config_test(self):
        return {
            "simulation": {
                "nombre_tours": 10,
                "pas_temps_minutes": 1.0
            },
            "reseau": {
                "routes": [
                    {"nom": "A1", "longueur": 1000, "limite_vitesse": 90},
                    {"nom": "A2", "longueur": 1500, "limite_vitesse": 110}
                ]
            },
            "vehicules": {
                "nombre_initial": 50,
                "taux_arrivee_par_tour": 5,
                "taux_depart_par_tour": 3
            }
        }

    @pytest.fixture
    def fichier_config_temporaire(self, config_test):
        """Crée un fichier de configuration temporaire."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config_test, f)
            temp_path = f.name
        yield temp_path
        Path(temp_path).unlink()

    # Tests d'initialisation du simulateur
    def test_chargement_config_depuis_fichier(self, fichier_config_temporaire):
        """Vérifie que la configuration est chargée correctement depuis un fichier."""
        config = charger_config(fichier_config_temporaire)

        assert config is not None
        assert "simulation" in config
        assert "reseau" in config
        assert "vehicules" in config
        assert config["simulation"]["nombre_tours"] == 10

    def test_config_contient_parametres_simulation(self, config_test):
        """Vérifie que la configuration contient tous les paramètres nécessaires."""
        assert "nombre_tours" in config_test["simulation"]
        assert "pas_temps_minutes" in config_test["simulation"]
        assert config_test["simulation"]["nombre_tours"] > 0
        assert config_test["simulation"]["pas_temps_minutes"] > 0

    # Tests d'exécution de la simulation
    def test_simulation_plusieurs_tours_sans_erreur(self, config_test):
        """Vérifie que la simulation s'exécute sur plusieurs tours sans erreur."""
        historique = simuler_trafic(config_test)

        assert historique is not None
        assert len(historique) == config_test["simulation"]["nombre_tours"]
        assert all("tour" in stat for stat in historique)

    def test_simulation_genere_statistiques_completes(self, config_test):
        """Vérifie que chaque tour génère des statistiques complètes."""
        historique = simuler_trafic(config_test)

        for stat in historique:
            assert "tour" in stat
            assert "temps_ecoule" in stat
            assert "nombre_vehicules" in stat
            assert "vitesse_moyenne" in stat
            assert "taux_congestion" in stat
            assert "details_routes" in stat

    # Tests alternatifs
    def test_analyse_resultats_genere_rapport(self, config_test):
        """Vérifie que l'analyse des résultats génère un rapport complet."""
        historique = simuler_trafic(config_test)
        rapport = analyser_resultats(historique)

        assert rapport is not None
        assert "resume_general" in rapport
        assert "congestion" in rapport
        assert "evolution_vehicules" in rapport
        assert "statistiques_routes" in rapport

    def test_simulation_avec_configuration_minimale(self):
        """Vérifie que la simulation fonctionne avec une configuration minimale."""
        config_minimal = {
            "simulation": {
                "nombre_tours": 3,
                "pas_temps_minutes": 1.0
            },
            "reseau": {
                "routes": [
                    {"nom": "Route1", "longueur": 500, "limite_vitesse": 50}
                ]
            },
            "vehicules": {
                "nombre_initial": 10,
                "taux_arrivee_par_tour": 2,
                "taux_depart_par_tour": 1
            }
        }

        historique = simuler_trafic(config_minimal)

        assert len(historique) == 3
        assert historique[0]["tour"] == 1
        assert historique[-1]["tour"] == 3
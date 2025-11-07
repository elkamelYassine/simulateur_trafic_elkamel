import pytest
from simulateur_trafic.models.reseau import ReseauRoutier
from simulateur_trafic.models.route import Route
from simulateur_trafic.models.vehicule import Vehicule


class TestReseau:
    """Tests pour la classe Reseau."""

    # Tests d'ajout de routes au réseau
    def test_ajout_route_fonctionne(self, route_simple):
        """Vérifie que l'ajout d'une route au réseau fonctionne correctement."""
        reseau = ReseauRoutier("Réseau Test")

        reseau.ajouter_route(route_simple)

        assert route_simple.nom in reseau.routes
        assert reseau.routes[route_simple.nom] == route_simple
        assert len(reseau.routes) == 1

    def test_ajout_plusieurs_routes(self):
        """Vérifie l'ajout de plusieurs routes au réseau."""
        reseau = ReseauRoutier("Réseau Test")
        route1 = Route("A1", longueur=100, limite_vitesse=90)
        route2 = Route("A2", longueur=150, limite_vitesse=110)
        route3 = Route("A3", longueur=80, limite_vitesse=70)

        reseau.ajouter_route(route1)
        reseau.ajouter_route(route2)
        reseau.ajouter_route(route3)

        assert len(reseau.routes) == 3
        assert "A1" in reseau.routes
        assert "A2" in reseau.routes
        assert "A3" in reseau.routes

    # Tests de mise à jour de l'ensemble des routes
    def test_mise_a_jour_incremente_temps(self, reseau_simple):
        """Vérifie que la mise à jour incrémente le temps écoulé."""
        temps_initial = reseau_simple.temps_ecoule

        reseau_simple.mettre_a_jour(delta_t=5.0)

        assert reseau_simple.temps_ecoule == temps_initial + 5.0

    def test_mise_a_jour_plusieurs_routes(self):
        """Vérifie que la mise à jour fonctionne avec plusieurs routes."""
        reseau = ReseauRoutier("Réseau Test")
        route1 = Route("A1", longueur=100, limite_vitesse=90)
        route2 = Route("A2", longueur=150, limite_vitesse=110)
        reseau.ajouter_route(route1)
        reseau.ajouter_route(route2)

        vehicule1 = Vehicule(vitesse_initiale=60.0, position_initiale=0.0, route_actuelle=route1)
        vehicule2 = Vehicule(vitesse_initiale=80.0, position_initiale=0.0, route_actuelle=route2)
        reseau.ajouter_vehicule(vehicule1, nom_route="A1")
        reseau.ajouter_vehicule(vehicule2, nom_route="A2")

        pos1_initiale = vehicule1.position
        pos2_initiale = vehicule2.position

        reseau.mettre_a_jour(delta_t=1.0)

        assert vehicule1.position > pos1_initiale
        assert vehicule2.position > pos2_initiale
        assert reseau.temps_ecoule == 1.0

    # Tests alternatifs
    def test_retrait_route_avec_vehicules(self, reseau_simple, route_simple, vehicule_exemple):
        """Vérifie que retirer une route retire aussi ses véhicules du réseau."""
        reseau_simple.ajouter_vehicule(vehicule_exemple, nom_route=route_simple.nom)

        reseau_simple.retirer_route(route_simple.nom)

        assert route_simple.nom not in reseau_simple.routes
        assert len(reseau_simple.vehicules) == 0

    def test_obtenir_statistiques_reseau_complet(self, reseau_simple, route_simple, vehicule_exemple):
        """Vérifie que les statistiques reflètent l'état du réseau."""
        reseau_simple.ajouter_vehicule(vehicule_exemple, nom_route=route_simple.nom)
        reseau_simple.mettre_a_jour(delta_t=3.0)

        stats = reseau_simple.obtenir_statistiques()

        assert stats["temps_ecoule"] == 3.0
        assert stats["nombre_routes"] == 1
        assert stats["nombre_vehicules"] >= 1
        assert "details_routes" in stats
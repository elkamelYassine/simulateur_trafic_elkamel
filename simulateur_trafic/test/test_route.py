import pytest
from simulateur_trafic.models.route import Route
from simulateur_trafic.models.vehicule import Vehicule


class TestRoute:
    """Tests pour la classe Route."""

    def test_ajout_vehicule_fonctionne(self, route_simple):
        """Vérifie que l'ajout d'un véhicule fonctionne correctement."""
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=0.0)

        resultat = route_simple.ajouter_vehicule(vehicule)

        assert resultat is True
        assert vehicule in route_simple.vehicules
        assert len(route_simple.vehicules) == 1
        assert vehicule.route_actuelle == route_simple

    def test_ajout_plusieurs_vehicules(self, route_simple):
        """Vérifie l'ajout de plusieurs véhicules sur la même route."""
        vehicule1 = Vehicule(vitesse_initiale=60.0, position_initiale=0.0)
        vehicule2 = Vehicule(vitesse_initiale=70.0, position_initiale=10.0)
        vehicule3 = Vehicule(vitesse_initiale=80.0, position_initiale=20.0)

        route_simple.ajouter_vehicule(vehicule1)
        route_simple.ajouter_vehicule(vehicule2)
        route_simple.ajouter_vehicule(vehicule3)

        assert len(route_simple.vehicules) == 3
        assert vehicule1 in route_simple.vehicules
        assert vehicule2 in route_simple.vehicules
        assert vehicule3 in route_simple.vehicules

    def test_ajout_vehicule_deja_presente_retourne_false(self, route_simple, vehicule_exemple):
        """Vérifie qu'ajouter un véhicule déjà présent retourne False."""
        route_simple.ajouter_vehicule(vehicule_exemple)

        resultat = route_simple.ajouter_vehicule(vehicule_exemple)

        assert resultat is False
        assert len(route_simple.vehicules) == 1

    def test_mise_a_jour_avance_les_vehicules(self, route_simple):
        """Vérifie que la mise à jour avance les véhicules sur la route."""
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=0.0, route_actuelle=route_simple)
        route_simple.ajouter_vehicule(vehicule)
        position_initiale = vehicule.position

        route_simple.mettre_a_jour_vehicules(delta_t=1.0)

        assert vehicule.position > position_initiale
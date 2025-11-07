import pytest

from simulateur_trafic.models.route import Route
from simulateur_trafic.models.vehicule import Vehicule
from simulateur_trafic.models.reseau import ReseauRoutier

@pytest.fixture
def route_simple():
    return Route("A1", longueur=1000, limite_vitesse=30)

@pytest.fixture
def vehicule_exemple(route_simple):
    return Vehicule(vitesse_initiale=50.0, position_initiale=0.0, route_actuelle=route_simple)

@pytest.fixture
def reseau_simple(route_simple, vehicule_exemple):
    reseau = ReseauRoutier()

    reseau.ajouter_route(route_simple)
    route_simple.ajouter_vehicule(vehicule_exemple)
    return reseau
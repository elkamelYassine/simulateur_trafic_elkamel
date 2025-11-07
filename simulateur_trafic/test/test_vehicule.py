import pytest
from simulateur_trafic.models.route import Route
from simulateur_trafic.models.vehicule import Vehicule


class TestVehicule:
    """Tests pour la classe Vehicule."""

    # Tests d'avancement
    def test_avancement_modifie_position(self):
        """Vérifie que l'avancement modifie correctement la position du véhicule."""
        route = Route("A1", longueur=100, limite_vitesse=60)
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=0.0, route_actuelle=route)
        position_initiale = vehicule.position

        vehicule.avancer(delta_t=1.0)

        assert vehicule.position > position_initiale
        assert vehicule.position == pytest.approx(1.0, rel=1e-2)

    def test_avancement_avec_vitesse_nulle(self):
        """Vérifie qu'un véhicule à l'arrêt ne bouge pas."""
        route = Route("A1", longueur=100, limite_vitesse=60)
        vehicule = Vehicule(vitesse_initiale=0.0, position_initiale=0.0, route_actuelle=route)

        vehicule.avancer(delta_t=1.0)

        assert vehicule.position == 0.0


    def test_avancement_met_a_jour_statistiques(self):
        """Vérifie que l'avancement met à jour les statistiques du véhicule."""

        route = Route("A1", longueur=100, limite_vitesse=60)
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=0.0, route_actuelle=route)

        vehicule.avancer(delta_t=5.0)

        assert vehicule.distance_parcourue > 0
        assert vehicule.temps_trajet == 5.0

    def test_avancement_sans_route(self):
        """Vérifie qu'un véhicule sans route ne peut pas avancer."""

        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=0.0, route_actuelle=None)
        position_initiale = vehicule.position

        vehicule.avancer(delta_t=1.0)

        assert vehicule.position == position_initiale


    def test_vehicule_ne_depasse_pas_longueur_route(self):
        """Vérifie que le véhicule s'arrête à la fin de la route."""
        route = Route("A1", longueur=10, limite_vitesse=60)
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=8.0, route_actuelle=route)

        vehicule.avancer(delta_t=10.0)

        assert vehicule.position <= route.longueur
        assert vehicule.position == route.longueur


    # Tests de changement de route
    def test_changement_route_remet_position_a_zero(self):
        """Vérifie que le changement de route remet la position à zéro."""
        route1 = Route("A1", longueur=100, limite_vitesse=60)
        route2 = Route("A2", longueur=150, limite_vitesse=80)
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=50.0, route_actuelle=route1)
        route1.ajouter_vehicule(vehicule)

        resultat = vehicule.changer_de_route(route2)

        assert resultat is True
        assert vehicule.position == 0.0
        assert vehicule.route_actuelle == route2



    def test_changement_route_null_retourne_false(self):
        """Vérifie que changer vers une route None retourne False."""
        route1 = Route("A1", longueur=100, limite_vitesse=60)
        vehicule = Vehicule(vitesse_initiale=60.0, position_initiale=0.0, route_actuelle=route1)

        resultat = vehicule.changer_de_route(None)


        assert resultat is False
        assert vehicule.route_actuelle == route1


    # Tests d'ajustement de vitesse
    def test_ajuster_vitesse_sans_vehicule_devant_accelere(self):
        """Vérifie que le véhicule accélère s'il n'y a personne devant."""

        route = Route("A1", longueur=100, limite_vitesse=80)
        vehicule = Vehicule(vitesse_initiale=50.0, position_initiale=0.0, route_actuelle=route)

        vehicule.ajuster_vitesse(None)

        assert vehicule.vitesse == 60.0


    def test_ajuster_vitesse_distance_raisonnable_adapte(self):
        """Vérifie que le véhicule adapte sa vitesse à distance raisonnable."""

        route = Route("A1", longueur=100, limite_vitesse=80)
        vehicule1 = Vehicule(vitesse_initiale=50.0, position_initiale=0.0, route_actuelle=route)
        vehicule2 = Vehicule(vitesse_initiale=60.0, position_initiale=0.07, route_actuelle=route)

        vehicule1.ajuster_vitesse(vehicule2, distance_securite=0.05)

        assert vehicule1.vitesse == vehicule2.vitesse


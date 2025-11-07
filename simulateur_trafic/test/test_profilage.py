import cProfile
import pstats
import io
import sys

from simulateur_trafic.models.reseau import ReseauRoutier
from simulateur_trafic.models.route import Route
from simulateur_trafic.models.vehicule import Vehicule
from simulateur_trafic.core.simulateur import Simulateur


def creer_reseau_test():
    """Crée un réseau routier simple avec 500 véhicules pour le test."""
    reseau = ReseauRoutier(nom="Test Réseau")
    route_A = Route("A1", 10.0, 110.0, 3)
    route_B = Route("B2", 8.0, 90.0, 2)
    reseau.ajouter_route(route_A)
    reseau.ajouter_route(route_B)
    reseau.connecter_routes("A1", "B2")

    for i in range(500):
        v = Vehicule(vitesse_initiale=80.0)
        if i % 2 == 0:
            reseau.ajouter_vehicule(v, "A1")
        else:
            reseau.ajouter_vehicule(v, "B2")

    return reseau


def test_profilage_simulation():
    """
    Lance la simulation avec cProfile et affiche les résultats.
    Pytest exécute cette fonction car elle commence par 'test_'.
    """
    pr = cProfile.Profile()
    pr.enable()


    reseau = creer_reseau_test()
    simulateur = Simulateur(reseau=reseau)
    # Lancer la simulation pendant 500 tours (500 minutes)
    simulateur.lancer_simulation(n_tours=500, delta_t=1.0, taux_arrivee=0.01, afficher_progression=False)

    pr.disable()


    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)

    sys.stdout.write("\n" + "=" * 80 + "\n")
    sys.stdout.write("       RAPPORT DE PROFILAGE CPROFILE (Top 10 par temps cumulé)      \n")
    sys.stdout.write("=" * 80 + "\n")
    ps.print_stats(10)
    sys.stdout.write(s.getvalue())

    s_tt = io.StringIO()
    sortby_tt = pstats.SortKey.TIME
    ps_tt = pstats.Stats(pr, stream=s_tt).sort_stats(sortby_tt)

    sys.stdout.write("\n" + "=" * 80 + "\n")
    sys.stdout.write("       RAPPORT DE PROFILAGE CPROFILE (Top 10 par temps propre)      \n")
    sys.stdout.write("=" * 80 + "\n")
    ps_tt.print_stats(10)
    sys.stdout.write(s_tt.getvalue())

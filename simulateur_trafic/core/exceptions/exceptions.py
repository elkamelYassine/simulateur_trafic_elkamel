"""
Module définissant les exceptions personnalisées pour la simulation de trafic.
"""

class ErreurSimulation(Exception):
    """
    Classe de base pour toutes les exceptions de la simulation.
    """
    pass

class ErreurReseau(ErreurSimulation):
    """
    Exception levée lors d'une erreur liée au réseau routier
    (ex: route non trouvée, connexion impossible).
    """
    def __init__(self, message: str):
        super().__init__(f"Erreur Réseau: {message}")

class ErreurConfiguration(ErreurSimulation):
    """
    Exception levée lors d'un problème de chargement ou de validation de la
    configuration (ex: fichier manquant, format invalide).
    """
    def __init__(self, fichier: str, message: str):
        super().__init__(f"Erreur Configuration dans {fichier}: {message}")


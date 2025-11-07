.. simulateur_traffic documentation master file, created by
   sphinx-quickstart on Fri Oct  3 11:35:39 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simulateur de Trafic Documentation
==================================

Bienvenue dans la documentation du simulateur de trafic. Ce projet fournit un système complet de simulation de trafic routier avec analyse des performances.

Description du Projet
---------------------

Le simulateur de trafic est un outil Python qui permet de simuler le comportement du trafic routier sur un réseau de routes. Il inclut :

* Simulation de véhicules sur différentes routes
* Analyse des performances du trafic
* Génération de rapports détaillés
* Export des données de simulation

Modules Principaux
------------------

.. toctree::
   :maxdepth: 2
   :caption: Documentation des Modules:

   modules/core
   modules/models
   modules/inputOutput

Guide d'Utilisation
-------------------

Pour utiliser le simulateur de trafic :

1. Configurez votre réseau de routes dans ``data/config_reseau.json``
2. Exécutez le script principal : ``python main.py``
3. Consultez les résultats dans le dossier ``resultats/``

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Référence API:

   api/simulateur_trafic.core
   api/simulateur_trafic.models
   api/simulateur_trafic.inputOutput

Indices et Tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

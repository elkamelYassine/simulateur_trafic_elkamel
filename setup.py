from setuptools import setup, find_packages
from Cython.Build import cythonize


setup(
    packages=find_packages(),

    ext_modules=cythonize([
        "simulateur_trafic/models/vehicule.pyx"
    ]),

    name='simulateur-trafic',
    version='1.0',
)
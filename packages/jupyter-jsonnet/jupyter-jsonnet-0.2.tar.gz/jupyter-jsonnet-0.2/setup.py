from setuptools import (
    find_packages,
    setup,
)

setup(
    name="jupyter-jsonnet",
#    packages=find_packages(),
    version="0.2",
    install_requires = ['jupyter-client'],
)

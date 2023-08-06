from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read()

setup(
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={
        "renku": ["bio = renkubio.cli"],
        "renku.cli_plugins": ["bio = renkubio.cli:bio"],
    },
)

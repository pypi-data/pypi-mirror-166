import codecs

from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read()
with codecs.open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    entry_points={
        "renku": ["bio = renkubio.cli"],
        "renku.cli_plugins": ["bio = renkubio.cli:bio"],
    },
)

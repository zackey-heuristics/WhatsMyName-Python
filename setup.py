"""
whatsmyname
"""
from gettext import install
from importlib.metadata import entry_points
from setuptools import setup, find_packages


setup(
    name="whatsmyname",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "whatmyname=whatsmyname.whatsmyname:main",
        ],
    },
    author="zackey-heuristics",
    description="whatsmyname-python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zackey-heuristics/WhatsMyName-Python"
)
    
    
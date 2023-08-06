# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ontogram']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'plantuml>=0.3.0,<0.4.0', 'rdflib>=6.2.0,<7.0.0']

entry_points = \
{'console_scripts': ['ontogram = ontogram.cli:main']}

setup_kwargs = {
    'name': 'ontogram',
    'version': '0.1.1',
    'description': 'Ontogram - an OWL ontology diagram generator.',
    'long_description': "# Ontogram\n\n[![PyPI version](https://badge.fury.io/py/ontogram.svg)](https://badge.fury.io/py/ontogram)\n\nAn OWL ontology diagram generator.\n\nCurrently it supports `owl:class`, `rdfs:subClassOf`, `owl:equivalentClass`, datatype properties and domain and range relationships. I am planning to add support for `owl:subClassOf` restrictions soon. \n\n\n## Example output\n\nThe output of [examples/tern-org.ttl](examples/tern-org.ttl).\n\n![generated ontology diagram](examples/tern-org.ttl.txt.png)\n\n\n## Installation\n\nInstall via PyPI for Python 3.\n\n```\npip3 install ontogram\n```\n\n\n## Usage\n\n### Command line application\n\n```\n$ ontogram --help\n\nUsage: ontogram [OPTIONS] ONTOLOGY_FILEPATH\n\n  Ontogram CLI is a tool to generate a diagram from an OWL ontology file.\n\nOptions:\n  --format ['turtle', 'xml', 'nt', 'n3']\n                                  RDF serialization of input file. Default is\n                                  turtle.\n  --help                          Show this message and exit.\n```\n\nUse Ontogram's CLI to generate diagrams of an OWL ontology.\n```\nontogram ontology.ttl\n```\n\nOutput will be 3 files, `ontology.ttl.txt`, `ontology.ttl.png`, `ontology.ttl.svg`.\n\nUse the --format option to specify the RDF serialization of the ontology if it is not Turtle.\n\n\n### Python library\n\nOntogram is a Python library and can be easily integrated with any existing Python application.\n\n```python\nfrom ontogram import Ontogram\n\n# First parameter accepts a file path to the OWL ontology. \n# Second parameter tells Ontogram what RDF format the OWL ontology is in.\nontogram = Ontogram('ontology.ttl', format='turtle')\n\n# Generate a PNG diagram from the OWl ontology and write to disk as 'ontology.ttl.txt'.\nontogram.png_file('ontology.ttl.txt')\n\n# Same as above, but as an SVG diagram. \nontogram.svg_file('ontology.ttl.svg')\n```\n\nSee the [examples](examples) directory for example outputs.\n",
    'author': 'Edmond Chuc',
    'author_email': 'edmond.chuc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/edmondchuc/ontogram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transformerx', 'transformerx.layers', 'transformerx.txplot']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.4.1,<0.5.0',
 'matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pytest>=7.1.2,<8.0.0',
 'tensorflow>=2.9.0,<3.0.0']

setup_kwargs = {
    'name': 'transformerx',
    'version': '1.0.0b1',
    'description': 'TransformerX is a python library for building transformer-based models using ready-to-use layers.',
    'long_description': '<div align="center">\n<h1><b>TransformerX</b></h1>\n<p><b>TransformerX</b> is a Python library for building transformer-based models.</p>\n<p>It comes with multiple building blocks and layers you need for creating your model.</p>\n</div>\n\n<div align="center">\n<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/emgraph">\n<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/transformerx">\n<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/tensorops/transformerx">\n<img alt="PyPI - Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg">\n<img alt="PyPI - License" src="https://img.shields.io/pypi/l/transformerx.svg">\n<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/transformerx.svg">\n\n[//]: # (<img alt="Status" src="https://img.shields.io/pypi/status/transformerx.svg">)\n<img alt="Commits" src="https://badgen.net/github/commits/tensorops/transformerx">\n<img alt="Commits" src="https://img.shields.io/badge/TensorFlow 2-FF6F00?style=flat&logo=tensorflow&logoColor=white">\n</div>\n\n<div>\n  <p>Join <a href="https://discord.gg/WGdPS5NJ"><b>TensorOps</b> community on Discord</a></p>\n</div>\n\n<div>\n  <h2>Installation</h2>\n  <p>Install the latest version of <b>TransformerX</b>:</p>\n    <b>Note:</b> Currently you need to build it from the source, but, we are actively working, and it will be ready to use soon\n  <pre>[not yet working] $ pip install transformerx</pre>\n</div>\n\n\n<div>\n<h3>Features</h3>\n\n- [x] Support CPU/GPU\n- [x] Vectorized operations\n- [x] Standard API\n\n</div>\n<h2>If you found it helpful, please give us a <span>:star:</span></h2>\n\n<div>\n<h2>License</h2>\n<p>Released under the Apache 2.0 license</p>\n</div>\n\n<div class="footer"><pre>Copyright &copy; 2021-2022 <b>TensorOps</b> Developers\n\n<a href="https://soran-ghaderi.github.io/">Soran Ghaderi</a> (soran.gdr.cs@gmail.com)\nfollow me on <a href="https://github.com/soran-ghaderi"><img alt="Github" src="https://img.shields.io/badge/GitHub-100000?&logo=github&logoColor=white"></a> <a href="https://twitter.com/soranghadri"><img alt="Twitter" src="https://img.shields.io/badge/Twitter-1DA1F2?&logo=twitter&logoColor=white"></a> <a href="https://www.linkedin.com/in/soran-ghaderi/"><img alt="Linkedin" src="https://img.shields.io/badge/LinkedIn-0077B5?&logo=linkedin&logoColor=white"></a>\n<br>\n<a href="https://uk.linkedin.com/in/taleb-zarhesh">Taleb Zarhesh</a> (taleb.zarhesh@gmail.com)\nfollow me on <a href="https://github.com/sigma1326"><img alt="Github" src="https://img.shields.io/badge/GitHub-100000?&logo=github&logoColor=white"></a> <a href="https://twitter.com/taleb__z"><img alt="Twitter" src="https://img.shields.io/badge/Twitter-1DA1F2?&logo=twitter&logoColor=white"></a> <a href="https://www.linkedin.com/in/taleb-zarhesh/"><img alt="Linkedin" src="https://img.shields.io/badge/LinkedIn-0077B5?&logo=linkedin&logoColor=white"></a>\n</pre>\n</div>\n',
    'author': 'Soran Ghaderi',
    'author_email': 'soran.gdr.cs@gmail.com',
    'maintainer': 'Soran Ghaderi',
    'maintainer_email': 'soran.gdr.cs@gmail.com',
    'url': 'https://github.com/tensorops/TransformerX',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)

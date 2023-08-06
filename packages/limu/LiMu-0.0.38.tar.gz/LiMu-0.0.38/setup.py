# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['limu']
install_requires = \
['hdbscan>=0.8,<0.9',
 'numpy>=1.23,<2.0',
 'pandas>=1.1,<2.0',
 'rawpy>=0.17,<0.18',
 'scikit-image>=0.19,<0.20',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.9,<2.0']

entry_points = \
{'console_scripts': ['limu = limu:cli']}

setup_kwargs = {
    'name': 'limu',
    'version': '0.0.38',
    'description': 'Tool to analyse images of cleared and trypan blue stained leaves to assess leaf damage.',
    'long_description': '\nTool to analyse images of cleared and trypan blue stained leaves to assess leaf damage.\n\nlimu_original.py is the program used for the original publication.\n\nlimu.py is updated to be somewhat flexible with project parameters outside the script itself. It might need tweaking to suit your project though.\n\nCurrently only works with Canon .cr2 raw images. If you have other types please let me know and I might add other formats.\n\n    usage: limu [-h] [-p PROJECT] [-i INDIR] [-v] [-r]\n\n    Tool to analyse images of cleared and troptophan stained leaves to assess leaf damage.\n\n    optional arguments:\n      -h, --help            show this help message and \n\n      -p PROJECT, --project PROJECT\n                            path to projects directory, if not supplied one will\n                            be requested interactively. If limu.conf file found in\n                            current working directory, this will be used\n\n      -i INDIR, --input-dir INDIR\n                            path to infile root directory\n\n      -v, --verbose         Print more stuff\n\n      -r, --recalculate     Force recalculation, NOT IMPLEMENTED\n\n\nMulaosmanovic, E., Lindblom, T.U.T., Bengtsson, M., Windstam, S.T., Mogren, L., Marttila, S., Stützel, H., Alsanius, B.W., 2020. High-throughput method for detection and quantification of lesions on leaf scale based on trypan blue staining and digital image analysis. Plant Methods 16, 62. https://doi.org/10.1186/s13007-020-00605-5\n\nFull source is available at \n[https://gitlab.com/thorgil/limu](https://gitlab.com/thorgil/limu)\n',
    'author': 'Tobias U. T. Lindblom',
    'author_email': 'None',
    'maintainer': 'Tobias U. T. Lindblom',
    'maintainer_email': 'tobias.lindblom@gmail.com',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)

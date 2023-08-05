# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsimplex']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Markdown>=3.4.1,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'tk-html-widgets>=0.4.0,<0.5.0',
 'ttkthemes>=3.2.2,<4.0.0']

entry_points = \
{'console_scripts': ['dsimplex = .dsimplex:main',
                     'dsimplex-gui = .dsimplex-gui:main:']}

setup_kwargs = {
    'name': 'dsimplex',
    'version': '0.2.0',
    'description': 'A simplex implementation in python',
    'long_description': '[![Codacy Badge](https://app.codacy.com/project/badge/Grade/5fd619053adf4ce88c4333e306aafa4a)](https://www.codacy.com/gh/terminaldweller/simplex/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=terminaldweller/simplex&amp;utm_campaign=Badge_Grade)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/terminaldweller/simplex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/terminaldweller/simplex/alerts/)\n\n# Simplex\n\nA python package that solve linear programming problems using the simplex method.<br/>\nFeatures:<br/>\n* The Problem is input into the program by a file containing python expression.<br/>\n* Solves both min and max problems(duh!).<br/>\n* Uses the big M method to find a basic feasible solution when there are none available in the original program.<br/>\n* Handles adding slack variables to convert the problem into standard form.<br/>\n* Uses the lexicographic rule to prevent ending up in a loop due to degenerate extreme points.<br/>\n* outputs in html.</br>\n\nRun Help to get a list of available commandline options.<br/>\n```sh\n./test.py --help                                                                                                                                                                             [INSERT] 32mS 0↵ L3\nusage: test.py [-h] [--equs EQUS] [--csv CSV] [--delim DELIM] [--slack SLACK] [--aux AUX] [--iter ITER] [--min] [--verbose] [--debug] [--out] [--numba]\n\noptions:\n  -h, --help            show this help message and exit\n  --equs EQUS, -e EQUS  the path to the file containing the equations\n  --csv CSV, -c CSV     the path to the CSV file containing the problem\n  --delim DELIM, -l DELIM\n                        the separator for the csv file\n  --slack SLACK, -s SLACK\n                        slack variable base name, names are cretedby adding a number to the string\n  --aux AUX, -a AUX     aux variable base name, names are cretedby adding a number to the string\n  --iter ITER, -i ITER  maximum number of iterations\n  --min, -m             determines whether its a minimization problem.if not, its a maximization problem\n  --verbose, -v         whether to print output verbosely\n  --debug, -d           whether to print debug info\n  --out, -o             path to the output file\n  --numba, -n           whether to print debug info]q\n```\n\nExample usage:<br/>\n```sh\ndsimplex -e ./tests/equ6.py -a xa -v -s z -m\n```\n\n## The Equation File\ndsimplex currently accepts two input formats:</br>\n\n### Python Expressions\nEach equation in the equations file should a valid python expression. There are a couple notes though:<br/>\n* For conditions that end in equality you must use `==` instead of `=` to make it a legal python expression.\n* Nothing will be evaluated so writing something like `4/5*x1` is illegal. Use `.8*x1` instead.\n* You can use comments inside the equations file. They are the same format as the python comments.\n* The cost equation is one without a binary comparison operator, e.g. `<=,<,>=,>`.\n* The order of the equations in the equations file is not important. You can put them in in any order you want.\nAs an example:<br/>\n```py\n# cyclic test\n-0.75 * x4 + 20 * x5 - 0.5 * x6 + 6 * x7\nx1 + 0.25 * x4 - 8 * x5 - x6 + 9 * x7 == 0\nx2 + 0.5 * x4 - 12 * x5 - 0.5 * x6 + 3 * x7 == 0\nx3 + x6 == 1\nx1 >= 0\nx2 >= 0\nx3 >= 0\nx4 >= 0\nx5 >= 0\nx6 >= 0\nx7 >= 0\n```\n\n### CSV\n* The order of the equations is not important. It is also not important where the cost function is in the csv file as long as it is there.\n* The variables with zero coefficients should be left empty.\n```csv\nx1,x2,x3,x4,x5,x6,x7,cond,rhs\n,,,-0.75,20,-0.5,6,,\n1,,,0.25,-8,-1,9,=,0\n,1,,0.5,-12,-0.5,3,=,0\n,,1,,,1,,=,1\n1,,,,,,,>=,0\n,1,,,,,,>=,0\n,,1,,,,,>=,0\n,,,1,,,,>=,0\n,,,,1,,,>=,0\n,,,,,1,,>=,0\n,,,,,,1,>=,0\n```\n```csv\nx1,x2,x3,x4,x5,x6,x7,cond,rhs\n,,,-0.75,20,-0.5,6,,\n1,,,0.25,-8,-1,9,=,0\n,1,,0.5,-12,-0.5,3,=,0\n,,1,,,1,,=,1\n1,,,,,,,>=,0\n,1,,,,,,>=,0\n,,1,,,,,>=,0\n,,,1,,,,>=,0\n,,,,1,,,>=,0\n,,,,,1,,>=,0\n,,,,,,1,>=,0\nnull,,,,,,,,\n,,,-0.75,20,-0.5,6,,\n1,,,0.25,-8,-1,9,=,0\n,1,,0.5,-12,-0.5,3,=,0\n,,1,,,1,,=,1\n1,,,,,,,>=,0\n,1,,,,,,>=,0\n,,1,,,,,>=,0\n,,,1,,,,>=,0\n,,,,1,,,>=,0\n,,,,,1,,>=,0\n,,,,,,1,>=,0\nnull,,,,,,,,\n,,,-0.75,20,-0.5,6,,\n1,,,0.25,-8,-1,9,=,0\n,1,,0.5,-12,-0.5,3,=,0\n,,1,,,1,,=,1\n1,,,,,,,>=,0\n,1,,,,,,>=,0\n,,1,,,,,>=,0\n,,,1,,,,>=,0\n,,,,1,,,>=,0\n,,,,,1,,>=,0\n,,,,,,1,>=,0\nnull,,,,,,,,\n,,,-0.75,20,-0.5,6,,\n1,,,0.25,-8,-1,9,=,0\n,1,,0.5,-12,-0.5,3,=,0\n,,1,,,1,,=,1\n1,,,,,,,>=,0\n,1,,,,,,>=,0\n,,1,,,,,>=,0\n,,,1,,,,>=,0\n,,,,1,,,>=,0\n,,,,,1,,>=,0\n,,,,,,1,>=,0\n```\n```csv\nx1,x2,x3,condition,rhs\n1,1,-4,,\n1,1,2,<=,9\n1,1,-1,<=,2\n-1,1,1,<=,4\n1,,,>=,0\n,1,,>=,0\n,,1,>=,0\nx1,x2,cond,rhs\n1,-2,,\n1,1,>=,2\n-1,1,>=,1\n,1,<=,3\n1,,>=,0\n,1,>=,0\nx1,x2,x3,x4,x5,x6,x7,cond,rhs\n,,,-0.75,20,-0.5,6,,\n1,,,0.25,-8,-1,9,=,0\n,1,,0.5,-12,-0.5,3,=,0\n,,1,,,1,,=,1\n1,,,,,,,>=,0\n,1,,,,,,>=,0\n,,1,,,,,>=,0\n,,,1,,,,>=,0\n,,,,1,,,>=,0\n,,,,,1,,>=,0\n,,,,,,1,>=,0\n```\n\n## How to Get\nYou can get it from [pypi](https://pypi.org/project/dsimplex/):<br/>\n```sh\npip3 install dsimplex\n```\nOr you can clone this repo and run it like that:<br/>\n```sh\ngit clone https://github.com/terminaldweller/simplex && cd simplex && poetry install\n```\n',
    'author': 'terminaldweller',
    'author_email': 'thabogre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/terminaldweller/simplex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

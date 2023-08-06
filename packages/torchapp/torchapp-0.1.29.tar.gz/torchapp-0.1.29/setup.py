# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchapp',
 'torchapp.callbacks',
 'torchapp.cookiecutter.tests',
 'torchapp.cookiecutter.{{cookiecutter.project_slug}}.docs',
 'torchapp.cookiecutter.{{cookiecutter.project_slug}}.tests',
 'torchapp.cookiecutter.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}',
 'torchapp.examples',
 'torchapp.tuning']

package_data = \
{'': ['*'],
 'torchapp': ['bibtex/*',
              'cookiecutter/*',
              'cookiecutter/.github/ISSUE_TEMPLATE/*',
              'cookiecutter/.github/workflows/*',
              'cookiecutter/{{cookiecutter.project_slug}}/*',
              'cookiecutter/{{cookiecutter.project_slug}}/.github/ISSUE_TEMPLATE/*',
              'cookiecutter/{{cookiecutter.project_slug}}/.github/workflows/*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'click==8.0.4',
 'cookiecutter>=2.1.1,<3.0.0',
 'fastai>=2.5.3,<3.0.0',
 'mlflow>=1.25.1,<2.0.0',
 'numpy>=1.22.0,<2.0.0',
 'optuna>=2.10.0,<3.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pybtex>=0.24.0,<0.25.0',
 'pybtexnbib>=0.1.1,<0.2.0',
 'pyjwt>=2.4.0',
 'rich>=10.16.1,<11.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scikit-optimize>=0.9.0,<0.10.0',
 'scipy>=1.9.1,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'typer>=0.4.0,<0.5.0',
 'wandb>=0.12.9,<0.13.0']

entry_points = \
{'console_scripts': ['torchapp = torchapp.main:app',
                     'torchapp-imageclassifier = '
                     'torchapp.examples.image_classifier:ImageClassifier.main']}

setup_kwargs = {
    'name': 'torchapp',
    'version': '0.1.29',
    'description': 'A wrapper for fastai projects to create easy command-line inferfaces and manage hyper-parameter tuning.',
    'long_description': 'None',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rbturnbull/torchapp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cf_pipelines',
 'cf_pipelines.base',
 'cf_pipelines.cli',
 'cf_pipelines.ml',
 'cf_pipelines.ml.contrib',
 'cf_pipelines.ml.contrib.metrics',
 'cf_pipelines.ml.project_template.{{cookiecutter.pipeline_slug}}',
 'cf_pipelines.serializers']

package_data = \
{'': ['*'], 'cf_pipelines.ml': ['project_template/*']}

install_requires = \
['cookiecutter',
 'mlflow>=1.26.0,<2.0.0',
 'ploomber>=0.19.2,<0.20.0',
 'typer>=0.4.1,<0.5.0']

extras_require = \
{'graphviz': ['pygraphviz>=1.9,<2.0']}

entry_points = \
{'console_scripts': ['pipelines = cf_pipelines.cli.__main__:main']}

setup_kwargs = {
    'name': 'code-first-pipelines',
    'version': '0.8.0',
    'description': 'A framework built on top of Ploomber that allows code-first definition of pipelines.',
    'long_description': 'Code-First Pipelines\n====================\n\nA framework built on top of [Ploomber](https://ploomber.io/) that allows code-first definition of pipelines. \n**No YAML needed!**  \n\n## Installation\n\nTBA\n\n## Usage\n\n### ML Pipelines\n\n```python\nimport pandas as pd\nfrom cf_pipelines.ml import MLPipeline\n\nmy_pipeline = MLPipeline("My Cool Pipeline")\n\n@my_pipeline.data_ingestion\ndef data_ingestion():\n    input_data = pd.read_csv(\'input_data.csv\')\n    adult_data = input_data[input_data[\'age\'] > 18]\n    return {\'adult_data.csv\':adult_data}\n\nmy_pipeline.run()\n```\n\nSee the [tutorial notebook](tutorials/Machine%20Learning%20Pipelines.ipynb) for a more comprehensive example.\n\n## Getting started with a template \n\nOnce installed, you can create a new pipeline template by running:\n\n```shell\npipelines new [pipeline name]\n```\n\n## Development\n\n### Extra dependencies\n\nThis project depends on Graphviz being installed in your system, follow the instructions [here](https://graphviz.org/download/).\n\nWe use [Poetry](https://python-poetry.org/) to manage this project\'s dependencies and virtual environment. \nOnce cloned, just run `poetry install` to install them. Any time you want to work on this project, just run \n`poetry shell` to activate the virtual environment, and you will be ready.\n\nWe use some tools to enforce code formatting. To make sure your code meets these standards, run `make fmt` (this will \nmodify the source files automatically) and then `make lint` to spot potential deficiencies.\n\nMake sure you add tests for any new code contributed to this repo, and make sure you run all the tests with `make test`\nbefore committing or opening a new pull request.\n',
    'author': 'Prediction and Learning at Simply Business',
    'author_email': 'pal@simplybusiness.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

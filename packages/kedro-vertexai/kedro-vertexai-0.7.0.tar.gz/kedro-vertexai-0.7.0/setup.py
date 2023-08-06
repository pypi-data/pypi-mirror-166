# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_vertexai', 'kedro_vertexai.auth', 'kedro_vertexai.vertex_ai']

package_data = \
{'': ['*'], 'kedro_vertexai': ['templates/*']}

install_requires = \
['cachetools>=4.1,<5.0',
 'click>=8.0.4',
 'fsspec>=2021.4,<=2022.1',
 'gcsfs>=2021.4,<=2022.1',
 'google-auth<3',
 'google-cloud-iam<3',
 'google-cloud-scheduler>=2.3.2',
 'google-cloud-storage<3.0.0',
 'grpcio-status>=1.44.0,<1.45.0',
 'grpcio>=1.44.0,<1.45.0',
 'kedro>=0.18.1,<0.19.0',
 'kfp>=1.8.12,<2.0',
 'protobuf<=3.20.0',
 'pydantic>=1.9.0,<1.10.0',
 'semver>=2.10,<3.0',
 'tabulate>=0.8.7']

extras_require = \
{'mlflow': ['kedro-mlflow>=0.11.1,<0.12.0']}

entry_points = \
{'kedro.hooks': ['vertexai_cfg_hook = '
                 'kedro_vertexai.hooks:env_templated_config_loader_hook',
                 'vertexai_mlflow_tags_hook = '
                 'kedro_vertexai.hooks:mlflow_tags_hook'],
 'kedro.project_commands': ['vertexai = kedro_vertexai.cli:commands'],
 'mlflow.request_header_provider': ['unused = '
                                    'kedro_vertexai.auth.mlflow_request_header_provider:DynamicMLFlowRequestHeaderProvider']}

setup_kwargs = {
    'name': 'kedro-vertexai',
    'version': '0.7.0',
    'description': 'Kedro plugin with GCP Vertex AI support',
    'long_description': '# Kedro Vertex AI Plugin\n\n[![Python Version](https://img.shields.io/pypi/pyversions/kedro-vertexai)](https://github.com/getindata/kedro-vertexai)\n[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![SemVer](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)\n[![PyPI version](https://badge.fury.io/py/kedro-vertexai.svg)](https://pypi.org/project/kedro-vertexai/)\n[![Downloads](https://pepy.tech/badge/kedro-vertexai)](https://pepy.tech/project/kedro-vertexai)\n\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-vertexai&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-vertexai)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-vertexai&metric=coverage)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-vertexai)\n[![Documentation Status](https://readthedocs.org/projects/kedro-vertexai/badge/?version=latest)](https://kedro-vertexai.readthedocs.io/en/latest/?badge=latest)\n\n## About\n\nThe main purpose of this plugin is to enable running kedro pipeline on Google Cloud Platform - Vertex AI Pipelines.\nIt supports translation from Kedro pipeline DSL to [kfp](https://www.kubeflow.org/docs/pipelines/sdk/sdk-overview/) \n(pipelines SDK) and deployment to Vertex AI service with some convenient commands.\n\nThe plugin can be used together with `kedro-docker` to simplify preparation of docker image for pipeline execution.   \n\n## Documentation\n\nFor detailed documentation refer to https://kedro-vertexai.readthedocs.io/\n\n## Usage guide \n\n```\nUsage: kedro vertexai [OPTIONS] COMMAND [ARGS]...\n\n  Interact with Google Cloud Platform :: Vertex AI Pipelines\n\nOptions:\n  -e, --env TEXT  Environment to use.\n  -h, --help      Show this message and exit.\n\nCommands:\n  compile         Translates Kedro pipeline into JSON file with Kubeflow...\n  init            Initializes configuration for the plugin\n  list-pipelines  List deployed pipeline definitions\n  run-once        Deploy pipeline as a single run within given experiment.\n  ui              Open VertexAI Pipelines UI in new browser tab\n```\n\n## Configuration file\n\n`kedro init` generates configuration file for the plugin, but users may want to adjust it to match the run environment \nrequirements. Check documentation for details - [kedro-vertexai.readthedocs.io](https://kedro-vertexai.readthedocs.io/en/latest/source/02_installation/02_configuration.html)\n',
    'author': 'Marcin Zabłocki',
    'author_email': 'marcin.zablocki@getindata.com',
    'maintainer': 'GetInData MLOPS',
    'maintainer_email': 'mlops@getindata.com',
    'url': 'https://github.com/getindata/kedro-vertexai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resoto']

package_data = \
{'': ['*']}

install_requires = \
['resoto-plugin-aws==2.4.1',
 'resoto-plugin-cleanup-aws-alarms==2.4.1',
 'resoto-plugin-cleanup-aws-loadbalancers==2.4.1',
 'resoto-plugin-cleanup-aws-vpcs==2.4.1',
 'resoto-plugin-cleanup-expired==2.4.1',
 'resoto-plugin-cleanup-untagged==2.4.1',
 'resoto-plugin-cleanup-volumes==2.4.1',
 'resoto-plugin-digitalocean==2.4.1',
 'resoto-plugin-example-collector==2.4.1',
 'resoto-plugin-gcp==2.4.1',
 'resoto-plugin-github==2.4.1',
 'resoto-plugin-k8s==2.4.1',
 'resoto-plugin-onelogin==2.4.1',
 'resoto-plugin-onprem==2.4.1',
 'resoto-plugin-protector==2.4.1',
 'resoto-plugin-slack==2.4.1',
 'resoto-plugin-tagvalidator==2.4.1',
 'resoto-plugin-vsphere==2.4.1',
 'resotocore==2.4.1',
 'resotometrics==2.4.1',
 'resotoshell==2.4.1',
 'resotoworker==2.4.1']

setup_kwargs = {
    'name': 'resoto',
    'version': '2.4.1',
    'description': 'Resoto bundle - single package for Resoto components',
    'long_description': 'Meta package containing all resoto components.\n\nInstallation:\n\n```\npip install resoto\n```',
    'author': 'Some Engineering Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/someengineering/resoto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
